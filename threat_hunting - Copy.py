import os
import logging
from datetime import datetime
from typing import List, Dict, Any
from collections import defaultdict
import random
import time
import json
import hashlib
import base64
import requests
import hmac
import threading
import platform
import subprocess
import ipaddress

from scapy.layers.inet import IP, TCP, UDP
from scapy.sendrecv import sniff

from flask import Flask, request, jsonify
from functools import wraps

from azure.identity import DefaultAzureCredential, AzureCliCredential
from azure.kusto.data import KustoClient, KustoConnectionStringBuilder
from azure.keyvault.secrets import SecretClient
from azure.kusto.data.exceptions import KustoServiceError


class ThreatHunting:
    def __init__(self, key_vault_uri: str, network_ranges: List[str] = None):
        """
        Initializes the ThreatHunting class with network_ranges and Key Vault URI.
        Retrieves Azure Sentinel workspace settings from Key Vault.

        Parameters:
        - key_vault_uri (str): The URI of the Azure Key Vault.
        - network_ranges (List[str], optional): List of network CIDR ranges to monitor.
        """
        self.network_ranges = network_ranges or ["0.0.0.0/0"]
        self.key_vault_uri = key_vault_uri
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(logging.INFO)

        # Configure logging handler
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(name)s: %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

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

        # Authenticate with Azure Kusto (Log Analytics) using service principal
        try:
            # Retrieve service principal credentials from Key Vault
            self.kusto_client_id = self.get_secret("AZURE-KUSTO-CLIENT-ID")
            self.kusto_client_secret = self.get_secret("AZURE-KUSTO-CLIENT-SECRET")
            self.kusto_tenant_id = self.get_secret("AZURE-TENANT-ID")

            if not all([self.kusto_client_id, self.kusto_client_secret, self.kusto_tenant_id]):
                raise ValueError("Kusto client credentials must be set in Key Vault.")

            kcsb = KustoConnectionStringBuilder.with_aad_application_key_authentication(
                self.kql_endpoint,
                self.kusto_client_id,
                self.kusto_client_secret,
                self.kusto_tenant_id
            )
            self.client = KustoClient(kcsb)
            self.logger.info("Authenticated to Azure Sentinel successfully.")
        except Exception as e:
            self.logger.exception(f"Failed to authenticate to Azure Sentinel: {e}")
            raise

        # Retrieve the primary key for Azure Monitor Data Collector API
        try:
            self.primary_key = self.get_secret("AZURE-SENTINEL-PRIMARY-KEY")
            if not self.primary_key:
                raise ValueError("AZURE-SENTINEL-PRIMARY-KEY must be set in Key Vault.")
            self.logger.info("Successfully retrieved primary key from Key Vault.")
        except Exception as e:
            self.logger.error(f"Failed to retrieve primary key: {e}")
            raise

        # Initialize API Key Management
        self.api_keys = self.get_api_keys()

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

    def add_blocked_port(self, port: int):
        """
        Adds a port number to the blocked list.

        Parameters:
        - port (int): The port number to block.
        """
        self.blocked_ports.add(port)
        self.logger.info(f"Added blocked port: {port}")

    def remove_blocked_port(self, port: int):
        """
        Removes a port number from the blocked list.

        Parameters:
        - port (int): The port number to unblock.
        """
        if port in self.blocked_ports:
            self.blocked_ports.discard(port)
            self.logger.info(f"Removed blocked port: {port}")
        else:
            self.logger.info(f"Port {port} is not in the blocked list.")

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

    def execute_query(self, database: str, query: str) -> List[Dict[str, Any]]:
        """
        Executes a Kusto Query Language (KQL) query against the specified database.

        Parameters:
        - database (str): The database name in Azure Data Explorer.
        - query (str): The KQL query to execute.

        Returns:
        - List[Dict[str, Any]]: The query results as a list of dictionaries.
        """
        try:
            response = self.client.execute(database, query)
            results = []
            for row in response.primary_results[0]:
                results.append(row.to_dict())
            self.logger.info(f"Kusto query executed successfully: {query}")
            return results
        except KustoServiceError as e:
            self.logger.error(f"Kusto query failed: {e}")
            return []
        except Exception as e:
            self.logger.exception(f"Unexpected error during Kusto query: {e}")
            return []

    def get_api_keys(self) -> List[str]:
        """
        Retrieves a list of valid API keys from Azure Key Vault.

        Returns:
        - List[str]: A list of API key strings.
        """
        try:
            # Assume API keys are stored with names like 'API-KEY-1', 'API-KEY-2', etc.
            api_keys = []
            for secret_properties in self.key_vault_client.list_properties_of_secrets():
                if secret_properties.name.startswith("API-KEY-"):
                    secret = self.key_vault_client.get_secret(secret_properties.name)
                    api_keys.append(secret.value)
            self.logger.info("Retrieved API keys from Key Vault.")
            return api_keys
        except Exception as e:
            self.logger.error(f"Failed to retrieve API keys: {e}")
            return []

    def validate_api_key(self, provided_key: str) -> bool:
        """
        Validates the provided API key against stored keys.

        Parameters:
        - provided_key (str): The API key provided by the client.

        Returns:
        - bool: True if valid, False otherwise.
        """
        hashed_provided_key = hashlib.sha256(provided_key.encode()).hexdigest()
        for key in self.api_keys:
            hashed_stored_key = hashlib.sha256(key.encode()).hexdigest()
            if hashed_provided_key == hashed_stored_key:
                self.logger.info("Valid API key provided.")
                return True
        self.logger.warning("Invalid API key provided.")
        return False

    def create_flask_app(self) -> Flask:
        """
        Creates and configures the Flask application with secure endpoints.

        Returns:
        - Flask: The configured Flask app.
        """
        app = Flask(__name__)

        def require_api_key(f):
            @wraps(f)
            def decorated(*args, **kwargs):
                api_key = request.headers.get('X-API-KEY')
                if not api_key or not self.validate_api_key(api_key):
                    self.logger.warning("Unauthorized access attempt detected.")
                    return jsonify({"error": "Unauthorized"}), 401
                return f(*args, **kwargs)
            return decorated

        @app.route('/add_blocked_ip', methods=['POST'])
        @require_api_key
        def add_ip():
            data = request.get_json()
            ip = data.get('ip')
            if not ip:
                return jsonify({"error": "IP address is required."}), 400
            if not self.is_valid_ip(ip):
                return jsonify({"error": "Invalid IP address format."}), 400
            self.add_blocked_ip(ip)
            return jsonify({"message": f"IP {ip} has been blocked."}), 200

        @app.route('/remove_blocked_ip', methods=['POST'])
        @require_api_key
        def remove_ip():
            data = request.get_json()
            ip = data.get('ip')
            if not ip:
                return jsonify({"error": "IP address is required."}), 400
            self.remove_blocked_ip(ip)
            return jsonify({"message": f"IP {ip} has been unblocked."}), 200

        @app.route('/add_blocked_port', methods=['POST'])
        @require_api_key
        def add_port():
            data = request.get_json()
            port = data.get('port')
            if port is None:
                return jsonify({"error": "Port number is required."}), 400
            try:
                port = int(port)
                if not (0 < port < 65536):
                    raise ValueError
            except ValueError:
                return jsonify({"error": "Invalid port number."}), 400
            self.add_blocked_port(port)
            return jsonify({"message": f"Port {port} has been blocked."}), 200

        @app.route('/remove_blocked_port', methods=['POST'])
        @require_api_key
        def remove_port():
            data = request.get_json()
            port = data.get('port')
            if port is None:
                return jsonify({"error": "Port number is required."}), 400
            try:
                port = int(port)
                if not (0 < port < 65536):
                    raise ValueError
            except ValueError:
                return jsonify({"error": "Invalid port number."}), 400
            self.remove_blocked_port(port)
            return jsonify({"message": f"Port {port} has been unblocked."}), 200

        return app
