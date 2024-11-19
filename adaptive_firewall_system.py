import os
import logging
import json
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
from cryptography.fernet import Fernet
import yaml
from scapy.all import sniff, IP
import sys
import threading
from compliance_manager import ComplianceManager
from auth_manager import QuantumLDAPAuthenticator
from siem_integration import SIEMIntegration
from threat_hunting_manager import ThreatHuntingManager
from traffic_analyzer import TrafficAnalyzer
from intrusion_detection_system import IntrusionDetectionSystem
from rule_manager import RuleManager
from policy_manager import PolicyManager
from threat_intelligence import ThreatIntelligence
from incident_responder import RealTimeIncidentResponder
from threat_hunting import ThreatHunting
from data_protection import DataProtection

# Setup logging
logging.basicConfig(level=logging.DEBUG)  # Set to DEBUG level for detailed output
logger = logging.getLogger(__name__)

def load_encryption_key(key_path='ox/ox_key.key'):
    try:
        with open(key_path, 'rb') as key_file:
            key = key_file.read()
        logger.info("Encryption key loaded successfully.")
        return key
    except FileNotFoundError:
        logger.error(f"Encryption key file '{key_path}' not found.")
        raise

def load_config_values(ox_file_path='ox/config.ox', key_path='ox/ox_key.key'):
    try:
        key = load_encryption_key(key_path)
        fernet = Fernet(key)

        with open(ox_file_path, 'rb') as ox_file:
            encrypted_data = ox_file.read()

        decrypted_config_str = fernet.decrypt(encrypted_data).decode()
        config = yaml.safe_load(decrypted_config_str)

        # Ensure required keys are present
        if not all(k in config for k in ("key_vault_uri", "network_ranges", "vault_name", "product_key")):
            logger.error(f"Missing required keys in the configuration file: {ox_file_path}")
            raise ValueError("Configuration file is missing required keys.")

        logger.info(f"Configuration successfully loaded from '{ox_file_path}'.")
        return config
    except Exception as e:
        logger.error(f"Failed to load configuration from '{ox_file_path}': {e}")
        raise


class AdaptiveFirewallSystem:
    def __init__(self, config):
        """
        Initialize the Adaptive Firewall System with necessary components.

        Args:
            config (dict): Configuration dictionary.
        """
        self.config = config

        # Retrieve Key Vault URI
        key_vault_uri = self.config.get("key_vault", {}).get("uri")
        if not key_vault_uri:
            raise ValueError("Key Vault URI is missing in the configuration.")

        # Retrieve Network Ranges
        self.network_ranges = self.config.get("network_ranges", [])

        # Retrieve Key Vault Name
        key_vault_name = self.config.get("key_vault_name")
        if not key_vault_name:
            raise ValueError("Key Vault name is required in the configuration.")
        
        missing_keys = [key for key in required_keys if key not in config or not config[key]]
        if missing_keys:
            logger.error(f"Missing required keys in configuration: {missing_keys}")
            raise ValueError(f"Missing keys: {', '.join(missing_keys)}")


        # Initialize Compliance Manager
        self.compliance_manager = ComplianceManager(config.get('compliance_standards', ['ISO27001', 'GDPR', 'HIPAA']))
        logger.info(f"ComplianceManager initialized with standards: {self.compliance_manager.standards}")

        self.auth_manager = QuantumLDAPAuthenticator(key_vault_uri, self.config.get("product_key"))
        # Initialize SIEM Integration
        try:
            self.siem_integration = SIEMIntegration(self.config.get('siem'))
            logger.info("SIEMIntegration initialized successfully.")
        except Exception as e:
            logger.error(f"Failed to initialize SIEM Integration: {e}")
            self.siem_integration = None

        # Initialize Threat Hunting Manager
        try:
            if self.siem_integration:
                self.threat_hunting_manager = ThreatHuntingManager(self.siem_integration)
                logger.info("ThreatHuntingManager initialized successfully.")
            else:
                logger.warning("SIEM Integration not initialized. Threat Hunting Manager will not be initialized.")
                self.threat_hunting_manager = None
        except Exception as e:
            logger.error(f"Failed to initialize Threat Hunting Manager: {e}")
            self.threat_hunting_manager = None

        # Set up Azure Key Vault client with DefaultAzureCredential
        credential = DefaultAzureCredential()
        self.key_vault_client = SecretClient(vault_url=key_vault_uri, credential=credential)

        # Initialize SIEM integration with Key Vault URI
        self.siem = SIEMIntegration(key_vault_uri=key_vault_uri, log_type="ApplicationLogs")

        # Initialize other components
        self.analyzer = TrafficAnalyzer()
        self.idps = IntrusionDetectionSystem()
        self.rule_manager = RuleManager()
        self.policy_manager = PolicyManager()
        self.threat_intel = ThreatIntelligence(self.get_secret("threat-feed-url"))
        self.logger = logging.getLogger('AdaptiveFirewallSystem')
        self.logger.setLevel(logging.INFO)
        self.incident_responder = RealTimeIncidentResponder()
        self.threat_hunting = ThreatHunting(key_vault_uri=key_vault_uri, network_ranges=self.network_ranges)
        self.data_protection = DataProtection()

    def get_secret(self, secret_name):
        """Retrieve a secret from Azure Key Vault."""
        try:
            secret = self.key_vault_client.get_secret(secret_name)
            logger.info(f"Successfully retrieved secret: {secret_name}")
            return secret.value
        except Exception as e:
            logger.error(f"Could not retrieve secret '{secret_name}': {e}")
            raise

    def initialize(self):
        """Initialize the system components."""
        try:
            # Load threat intelligence
            threat_data = self.threat_intel.fetch_threats()
            for threat in threat_data:
                self.rule_manager.add_rule({"src_ip": threat.get("ip"), "action": "block"})

            # Train models
            sniff(prn=self.analyzer.collect_training_data, count=100)
            self.analyzer.train_model()
            self.idps.anomaly_model.fit(self.analyzer.training_data)

            # Check if start_dashboard is defined before calling
            try:
                threading.Thread(target=start_dashboard).start()
            except NameError:
                logger.warning("start_dashboard function is not defined.")
        except Exception as e:
            logger.error(f"Error during initialization: {e}")

# Usage example
if __name__ == "__main__":
    try:
        # Load configuration from .ox file
        config = load_config_values()

        # Debugging: Print loaded configuration
        logger.debug(f"Loaded Configuration: {config}")

        # Initialize the Adaptive Firewall System
        firewall = AdaptiveFirewallSystem(config=config)
        logger.info("AdaptiveFirewallSystem initialized successfully.")

        # Start the firewall processes
        firewall.initialize()
        # You can add other methods to run specific components, such as firewall.monitor_traffic()

    except ValueError as e:
        logger.error(f"Configuration error: {e}")
    except Exception as e:
        logger.error(f"Failed to initialize AdaptiveFirewallSystem: {e}")
