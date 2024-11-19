import logging
from datetime import datetime
from typing import List, Dict, Any
import random
import json
import hashlib
import threading
import time
import yaml
from flask import Flask
from qsql import QSQL  # Assuming QSQL is now the new SQL manager
from roundtable_api import RoundTableAPI
import base64
import requests
import hmac
import binascii
import ipaddress
import platform
import subprocess
from scapy.layers.inet import IP, TCP, UDP
from scapy.sendrecv import sniff
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

class ThreatHunting:
    def __init__(self, key_vault_uri: str, network_ranges: list = None, sql_config: dict = None):
        """
        Initializes the ThreatHunting class with Azure SQL support via QSQL.

        Parameters:
        - key_vault_uri (str): The URI of the Azure Key Vault.
        - network_ranges (list, optional): List of network CIDR ranges to monitor.
        - sql_config (dict): Configuration dictionary for QSQL.
         - roundtable_api: Instance of RoundTableAPI for API interactions.
        """
        
        self.network_ranges = network_ranges or ["0.0.0.0/0"]
        self.key_vault_uri = key_vault_uri
        self.roundtable_api = roundtable_api

        # Logging setup
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(name)s: %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

        # Initialize QSQL
        try:
            self.sql_manager = QSQL(sql_config)
            self.sql_manager.open_connection()
            self.logger.info("QSQL initialized and connected.")
        except Exception as e:
            self.logger.error(f"Failed to initialize QSQL: {e}")
            raise

        # Initialize blocked IPs and ports
        self.blocked_ips = set()
        self.blocked_ports = set()

        # Initialize field vectors
        self.field_vectors = self.initialize_field_vectors()

        # Set up Key Vault client to retrieve Azure Sentinel workspace information
        credential = AzureCliCredential()
        self.key_vault_client = SecretClient(vault_url=self.key_vault_uri, credential=credential)

        # Retrieve workspace details from Key Vault
        try:
            self.workspace_id = self.get_secret("AZURE-SENTINEL-WORKSPACE-ID")
            self.workspace_region = self.get_secret("AZURE-SENTINEL-WORKSPACE-REGION")
        except Exception as e:
            self.logger.error(f"Failed to retrieve workspace details: {e}")
            raise

        if not self.workspace_id or not self.workspace_region:
            raise ValueError("AZURE-SENTINEL-WORKSPACE-ID and AZURE-SENTINEL-WORKSPACE-REGION must be set in Key Vault.")

        # Correctly construct the Kusto (ADX) endpoint
        self.kql_endpoint = f"https://{self.workspace_id}.{self.workspace_region}.kusto.windows.net"

        # Construct the Azure Monitor HTTP Data Collector API endpoint
        self.log_endpoint = f"https://{self.workspace_id}.ods.opinsights.azure.com/api/logs?api-version=2016-04-01"
        self.logger.info(f"ThreatHunting initialized with log endpoint: {self.log_endpoint}")


        # Retrieve the primary key for Azure Monitor Data Collector API
        try:
            self.primary_key = self.get_secret("AZURE-SENTINEL-PRIMARY-KEY")
            if not self.primary_key:
                raise ValueError("AZURE-SENTINEL-PRIMARY-KEY must be set in Key Vault.")
            self.logger.info("Successfully retrieved primary key from Key Vault.")
        except Exception as e:
            self.logger.error(f"Failed to retrieve primary key: {e}")
            raise

    def execute_sql_query(self, query: str, params: list = None):
        """
        Executes a SQL query using QSQL and returns the result.

        Parameters:
        - query (str): The SQL query to execute.
        - params (list, optional): Parameters for the query.

        Returns:
        - List[dict]: The query results.
        """
        try:
            results = self.sql_manager.execute_query(query, params)
            self.logger.info(f"Query executed successfully. Rows retrieved: {len(results)}")
            return results
        except Exception as e:
            self.logger.error(f"Failed to execute query: {e}")
            raise

    def log_to_sql(self, log_data: dict):
        """
        Logs data into an Azure SQL database using QSQL.

        Parameters:
        - log_data (dict): The structured log data to store.
        """
        query = """
        INSERT INTO ThreatLogs (event, protocol, source_ip, destination_ip, source_port, destination_port, timestamp)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        params = [
            log_data["event"],
            log_data["protocol"],
            log_data["source_ip"],
            log_data["destination_ip"],
            log_data["source_port"],
            log_data["destination_port"],
            log_data["timestamp"]
        ]
        try:
            self.sql_manager.execute_non_query(query, params)
            self.logger.info("Log data successfully stored in Azure SQL.")
        except Exception as e:
            self.logger.error(f"Failed to log data to Azure SQL: {e}")
            raise

    def shutdown(self):
        """Closes connections and performs cleanup."""
        try:
            self.sql_manager.close_connection()
            self.logger.info("ThreatHunting resources cleaned up.")
        except Exception as e:
            self.logger.error(f"Error during cleanup: {e}")

    def packet_callback(self, packet):
        """
        Callback function for processing each sniffed packet.
        Determines whether to block or allow the packet based on predefined rules.

        Parameters:
        - packet: The sniffed packet.
        """
        # Process only IP packets
        if IP in packet:
            src_ip = packet[IP].src
            dst_ip = packet[IP].dst
            protocol = packet[IP].proto

            # Identify the protocol (TCP, UDP, ICMP, etc.)
            if TCP in packet:
                protocol = 'TCP'
                src_port = packet[TCP].sport
                dst_port = packet[TCP].dport
            elif UDP in packet:
                protocol = 'UDP'
                src_port = packet[UDP].sport
                dst_port = packet[UDP].dport
            else:
                protocol = f"Protocol-{protocol}"
                src_port = None
                dst_port = None

            # Inhibition logic: Block if source IP is in blocked list or destination port is blocked
            should_block = False
            if src_ip in self.blocked_ips:
                should_block = True
            if dst_port in self.blocked_ports:
                should_block = True

            if should_block:
                self.logger.info(f"Packet Blocked: {protocol} from {src_ip} to {dst_ip}:{dst_port}")
                # Implement actual blocking mechanisms if applicable (requires OS-level permissions)
                self.block_ip(src_ip)
            else:
                self.logger.info(f"Packet Allowed: {protocol} from {src_ip} to {dst_ip}:{dst_port}")
                # Log the packet
                log_data = {
                    "event": "Packet Allowed",
                    "protocol": protocol,
                    "source_ip": src_ip,
                    "destination_ip": dst_ip,
                    "source_port": src_port,
                    "destination_port": dst_port,
                    "timestamp": datetime.utcnow().isoformat()
                }
                self.send_to_azure(log_data)

    def monitor_traffic(self):
        """
        Starts the traffic monitoring using Scapy's sniffing functionality.
        """
        self.logger.info("Starting traffic monitoring.")
        try:
            # Capture only IP packets
            sniff(filter="ip", prn=self.packet_callback, store=False)
        except Exception as e:
            self.logger.error(f"Error during traffic monitoring: {e}")

    def add_blocked_ip(self, ip: str):
        """
        Adds an IP address to the blocked list and blocks it using the firewall.

        Parameters:
        - ip (str): The IP address to block.
        """
        if not self.is_valid_ip(ip):
            self.logger.error(f"Invalid IP address format: {ip}")
            return

        self.blocked_ips.add(ip)
        self.logger.info(f"Added blocked IP: {ip}")
        self.block_ip(ip)

    def remove_blocked_ip(self, ip: str):
        """
        Removes an IP address from the blocked list and unblocks it using the firewall.

        Parameters:
        - ip (str): The IP address to unblock.
        """
        if ip in self.blocked_ips:
            self.unblock_ip(ip)
            self.blocked_ips.discard(ip)
            self.logger.info(f"Removed blocked IP: {ip}")
        else:
            self.logger.info(f"IP {ip} is not in the blocked list.")


    def initialize_field_vectors(self) -> Dict[str, List[float]]:
        """
        Initializes field vectors for each network range with entangled connections.
        Simulates bivoral duovector causality and data circulation.

        Returns:
        - Dict[str, List[float]]: A dictionary mapping network ranges to their field vectors.
        """
        field_vectors = {}
        entanglement_map = defaultdict(list)

        # Generate initial field vectors with random values
        for network in self.network_ranges:
            vector = [random.random() for _ in range(10)]
            field_vectors[network] = vector
            self.logger.info(f"Initialized base vector for network {network}: {vector}")

        # Establish entangled connections between vectors (cross-links)
        for network_a in self.network_ranges:
            for network_b in self.network_ranges:
                if network_a != network_b:
                    # Create entangled relationships by cross-influencing vector elements
                    entanglement_map[network_a].append(network_b)
                    # Update vectors with entangled values (simulating causality)
                    for i in range(len(field_vectors[network_a])):
                        # Influence vector in network_a by random entangled data from network_b
                        entangled_value = (field_vectors[network_a][i] + field_vectors[network_b][i]) / 2
                        field_vectors[network_a][i] = entangled_value

        # Log the final entangled field vectors
        for network, vector in field_vectors.items():
            self.logger.info(f"Entangled vector for network {network}: {vector}")

        # Store entanglement map for potential causal interactions
        self.entanglement_map = entanglement_map
        self.logger.info("Field vectors initialized with entangled connections for causal interactions.")
        return field_vectors

    def monitor_causal_influence(self):
        """
        Monitors and dynamically adjusts field vectors based on causal interactions and entanglement.
        """
        self.logger.info("Monitoring causal influence across entangled field vectors.")
        for network, entangled_networks in self.entanglement_map.items():
            for entangled_network in entangled_networks:
                # Check influence from entangled network and adjust accordingly
                influence_factor = random.uniform(0.1, 0.5)
                self.logger.info(f"Applying influence from {entangled_network} to {network}")
                for i in range(len(self.field_vectors[network])):
                    # Apply bivoral duovector causality, where each vector adapts based on its entangled counterpart
                    self.field_vectors[network][i] += influence_factor * (self.field_vectors[entangled_network][i] - self.field_vectors[network][i])

        # Log updated field vectors after applying causal interactions
        for network, vector in self.field_vectors.items():
            self.logger.info(f"Updated field vector for network {network} after causal influence: {vector}")

    def preprocess_data(self):
        """
        Preprocess network data to set up penetration sniffers based on field vectors.
        """
        for network, vector in self.field_vectors.items():
            self.logger.info(f"Preprocessing data for network {network} with vector {vector}")

    def quantum_numscore_hash(self, data: str) -> str:
        """
        Generates a quantum-inspired hash based on data to identify anomalies.

        Parameters:
        - data (str): The input data.

        Returns:
        - str: The SHA-256 hash of the data.
        """
        hasher = hashlib.sha256()
        hasher.update(data.encode())
        return hasher.hexdigest()

    def infiltration_response(self, network: str, threat_type: str):
        """
        Responds to an identified infiltration threat by isolating the network.

        Parameters:
        - network (str): The network range where the threat was detected.
        - threat_type (str): The type of threat detected.
        """
        self.logger.warning(f"Infiltration detected in network {network} due to {threat_type}")
        # Implement isolation or logging response mechanisms here
        self.logger.info(f"Isolating network {network} from the main system as a response to {threat_type}")
        # Example: Add the network to the blocked list
        self.block_ip(network)

    def send_to_azure(self, log_data: Dict[str, Any]):
        """
        Sends log data to Azure Sentinel (Azure Monitor) using the HTTP Data Collector API.

        Parameters:
        - log_data (Dict[str, Any]): The structured log data to send.
        """
        try:
            content_type = 'application/json'
            method = 'POST'
            resource = '/api/logs'
            rfc1123date = datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')
            body = json.dumps(log_data)
            content_length = len(body)

            # Build the signature
            signature = self.build_signature(rfc1123date, content_length, method, content_type, resource)

            headers = {
                'Authorization': signature,
                'Content-Type': content_type,
                'Log-Type': 'ThreatHuntingLogs',
                'x-ms-date': rfc1123date,
                'time-generated-field': 'Timestamp'
            }

            response = requests.post(self.log_endpoint, headers=headers, data=body)
            response.raise_for_status()
            self.logger.info(f"Successfully sent log to Azure Sentinel with status code {response.status_code}")
        except requests.exceptions.RequestException as e:
            self.logger.exception(f"Failed to send log to Azure Sentinel: {e}")

    def build_signature(self, rfc1123date: str, content_length: int, method: str, content_type: str, resource: str) -> str:
        """
        Builds the authorization signature for Azure HTTP Data Collector API.

        Parameters:
        - rfc1123date (str): The date in RFC1123 format.
        - content_length (int): The length of the content.
        - method (str): HTTP method (e.g., POST).
        - content_type (str): The content type of the request.
        - resource (str): The API resource path.

        Returns:
        - str: The authorization signature.
        """
        try:
            string_to_hash = f"{method}\n{content_length}\n{content_type}\nx-ms-date:{rfc1123date}\n{resource}"
            bytes_to_hash = string_to_hash.encode('utf-8')
            decoded_key = base64.b64decode(self.primary_key)
            hashed = hmac.new(decoded_key, bytes_to_hash, hashlib.sha256)
            encoded_hash = base64.b64encode(hashed.digest()).decode('utf-8')
            return f"SharedKey {self.workspace_id}:{encoded_hash}"
        except Exception as e:
            self.logger.error(f"Error building signature: {e}")
            raise

    def get_secret(self, secret_name: str) -> str:
        """
        Retrieves a secret from Azure Key Vault.

        Parameters:
        - secret_name (str): The name of the secret to retrieve.

        Returns:
        - str: The value of the secret.
        """
        try:
            secret = self.key_vault_client.get_secret(secret_name)
            self.logger.info(f"Successfully retrieved secret: {secret_name}")
            return secret.value
        except Exception as e:
            self.logger.error(f"Could not retrieve secret '{secret_name}': {e}")
            raise

    def rotate_secret_key(self):
        """
        Rotate the secret key and invalidate all existing API keys.
        """
        new_secret_key = hashlib.sha256(uuid.uuid4().bytes).hexdigest()
        self.secret_key = new_secret_key
        self.api_keys.clear()
        # Update the secret key in the configuration file or secure storage
        self.logger.info(f"New secret key: {self.secret_key}")
        # You may need to update Key Vault with the new secret_key

    def run(self):
        """
        Runs the Flask app and starts the threat hunting monitoring in separate threads.
        """
        # Start Flask app in a separate thread
        flask_thread = threading.Thread(target=lambda: self.app.run(host='0.0.0.0', port=5000))
        flask_thread.daemon = True
        flask_thread.start()

        # Start ThreatHunting traffic monitoring
        self.threat_hunting.monitor_traffic()


        # Flask App for additional functionality
app = Flask(__name__)

@app.route('/')
def home():
    return "Threat Hunting Service is running."

if __name__ == "__main__":
    # Load configuration
    with open("config.yaml", "r") as f:
        config = yaml.safe_load(f)

    sql_config = config.get("azure_sql", {})

    # Initialize ThreatHunting
    threat_hunting = ThreatHunting(key_vault_uri=config.get("key_vault_uri"), sql_config=sql_config)

    try:
        # Example query execution
        example_query = "SELECT * FROM ThreatLogs"
        results = threat_hunting.execute_sql_query(example_query)
        print(results)

        # Example logging
        log_data = {
            "event": "Packet Allowed",
            "protocol": "TCP",
            "source_ip": "192.168.1.1",
            "destination_ip": "192.168.1.2",
            "source_port": 12345,
            "destination_port": 80,
            "timestamp": datetime.utcnow().isoformat()
        }
        threat_hunting.log_to_sql(log_data)
    finally:
        threat_hunting.shutdown()

    app.run(debug=True)




