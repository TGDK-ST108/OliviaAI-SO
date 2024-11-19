import json
import logging
import hashlib
import hmac
import base64
import requests
from datetime import datetime
from azure.identity import AzureCliCredential
from azure.keyvault.secrets import SecretClient
from azure.eventhub import EventHubProducerClient, EventData
from cryptography.fernet import Fernet
import os

# Set up global logging configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load encryption key
def load_encryption_key(key_path="config/ox_key.key"):
    try:
        with open(key_path, "rb") as key_file:
            key = key_file.read()
        logger.info("Encryption key loaded successfully.")
        return key
    except FileNotFoundError:
        logger.error(f"Encryption key file '{key_path}' not found.")
        raise

# Load and decrypt configuration from .ox file
def load_config_from_ox(ox_file_path="config/config.ox", key=None):
    try:
        if key is None:
            key = load_encryption_key()

        # Initialize Fernet with the key
        fernet = Fernet(key)

        # Read and decrypt the .ox file
        with open(ox_file_path, "rb") as ox_file:
            encrypted_data = ox_file.read()
        decrypted_data = fernet.decrypt(encrypted_data).decode()

        # Parse the JSON configuration
        config = json.loads(decrypted_data)
        logger.info("Configuration loaded and decrypted successfully.")
        return config
    except Exception as e:
        logger.error(f"Failed to load configuration from '{ox_file_path}': {e}")
        raise

# Initialize configuration and retrieve Key Vault URI
try:
    config = load_config_from_ox()
    key_vault_uri = config.get("key_vault", {}).get("uri", "").strip()
    if not key_vault_uri.startswith("https://"):
        logger.error("Key Vault URI is missing or invalid.")
        raise ValueError("Key Vault URI must be a valid HTTPS URL string")
    logger.info(f"Retrieved Key Vault URI from config: {key_vault_uri}")
except Exception as e:
    logger.error(f"Failed to load configuration or Key Vault URI: {e}")
    raise

class SIEMIntegration:
    def __init__(self, config, use_event_hub=True):
        self.config = config  # Assign the config passed to the constructor
        self.use_event_hub = use_event_hub

        # Fetch Event Hub connection settings from the config
        self.event_hub_connection_str = config.get("event_hub", {}).get("connection_string", "").strip()
        self.event_hub_name = config.get("event_hub", {}).get("name", "").strip()

        # Initialize Event Hub producer if enabled and settings are present
        if self.use_event_hub and self.event_hub_connection_str and self.event_hub_name:
            self._initialize_event_hub_producer()
        else:
            self.event_hub_producer = None
            logger.info("Event Hub is disabled or configuration is missing.")

        # Initialize Key Vault Client
        try:
            credential = AzureCliCredential()
            self.key_vault_client = SecretClient(vault_url=key_vault_uri, credential=credential)
            logger.info("Initialized Azure Key Vault client successfully.")
        except Exception as e:
            logger.error(f"Failed to initialize Key Vault client: {e}")
            raise

        # Retrieve secrets from Key Vault
        self.workspace_id = self.get_secret("AZURE-SENTINEL-WORKSPACE-ID")
        self.primary_key = self.get_secret("AZURE-SENTINEL-PRIMARY-KEY")
        self.log_type = self.config.get("log_type", "SteelOx")

        # Initialize Log Analytics endpoint
        if self.workspace_id:
            self.log_endpoint = f"https://{self.workspace_id}.ods.opinsights.azure.com/api/logs?api-version=2016-04-01"
            logger.info(f"Initialized Log Analytics endpoint: {self.log_endpoint}")
        else:
            raise ValueError("Workspace ID is missing or invalid in Key Vault.")

    def _initialize_event_hub_producer(self):
        """Initializes the Event Hub producer."""
        try:
            self.event_hub_producer = EventHubProducerClient.from_connection_string(
                conn_str=self.event_hub_connection_str,
                eventhub_name=self.event_hub_name
            )
            logger.info(f"Initialized Event Hub producer for '{self.event_hub_name}'.")
        except Exception as e:
            logger.error(f"Failed to initialize Event Hub producer: {e}")
            raise

    def get_secret(self, secret_name, default=None):
        """Retrieve a secret from Azure Key Vault."""
        try:
            secret = self.key_vault_client.get_secret(secret_name)
            logger.info(f"Successfully retrieved secret: {secret_name}")
            return secret.value
        except Exception as e:
            if default is not None:
                logger.warning(f"Could not retrieve secret '{secret_name}': {e}. Using default value.")
                return default
            logger.error(f"Could not retrieve secret '{secret_name}': {e}")
            raise

    def log_event(self, message, level, destinations, **kwargs):
        """Logs an event to specified destinations."""
        log_entry = {
            "message": message,
            "level": level,
            "timestamp": datetime.utcnow().isoformat(),
            **kwargs,
        }
        logger.info(f"Logging event: {log_entry}")
        if "log_analytics" in destinations:
            self.send_to_log_analytics(log_entry)
        if "event_hub" in destinations and self.event_hub_producer:
            self.send_to_event_hub(log_entry)

    def send_to_log_analytics(self, log_entry):
        """Send logs to Azure Log Analytics."""
        try:
            body = json.dumps(log_entry)
            signature = self._build_signature(body)
            headers = {
                "Content-Type": "application/json",
                "Authorization": signature,
                "Log-Type": self.log_type,
                "x-ms-date": datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT"),
            }
            response = requests.post(self.log_endpoint, data=body, headers=headers)
            if response.status_code == 200:
                logger.info("Log successfully sent to Log Analytics.")
            else:
                logger.error(f"Failed to send log to Log Analytics: {response.status_code} - {response.text}")
        except Exception as e:
            logger.error(f"Error sending log to Log Analytics: {e}")

    def _build_signature(self, body):
        """Builds the authorization signature for Azure Log Analytics."""
        x_ms_date = datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT")
        string_to_hash = f"POST\n{len(body)}\napplication/json\nx-ms-date:{x_ms_date}\n/api/logs"
        hashed = hmac.new(base64.b64decode(self.primary_key), string_to_hash.encode("utf-8"), hashlib.sha256)
        signature = base64.b64encode(hashed.digest()).decode()
        return f"SharedKey {self.workspace_id}:{signature}"

    def send_to_event_hub(self, log_entry):
        """Send logs to Azure Event Hub."""
        try:
            event_data = EventData(json.dumps(log_entry))
            with self.event_hub_producer:
                self.event_hub_producer.send_batch([event_data])
            logger.info("Log successfully sent to Event Hub.")
        except Exception as e:
            logger.error(f"Error sending log to Event Hub: {e}")

# Example usage:
if __name__ == "__main__":
    try:
        siem_integration = SIEMIntegration(config=config, use_event_hub=True)
        siem_integration.log_event(
            message="User login successful",
            level="INFO",
            destinations=['log_analytics', 'event_hub'],
            User="steeloxsuperuser",
            Status="Success"
        )
    except Exception as e:
        logger.exception(f"Failed to initialize SIEMIntegration or send logs: {e}")
