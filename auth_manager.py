import os
import logging
import json
from azure.identity import DefaultAzureCredential, ClientSecretCredential
from azure.keyvault.secrets import SecretClient
from azure.core.exceptions import HttpResponseError, ClientAuthenticationError, ResourceNotFoundError
from cryptography.fernet import Fernet

# Setup logging
logging.basicConfig(level=logging.DEBUG)  # Set to DEBUG level for detailed output
logger = logging.getLogger(__name__)

# Load the key for decrypting .ox file
def load_encryption_key(key_path='ox/ox_key.key'):
    try:
        with open(key_path, 'rb') as key_file:
            key = key_file.read()
        logger.info("Encryption key loaded successfully.")
        return key
    except FileNotFoundError:
        logger.error(f"Encryption key file '{key_path}' not found.")
        raise

# Load Key Vault URI from an .ox file
def load_config_values(ox_file_path='ox/config.ox', key=None):
    try:
        if key is None:
            key = load_encryption_key()

        fernet = Fernet(key)

        with open(ox_file_path, 'rb') as ox_file:
            encrypted_data = ox_file.read()

        decrypted_config_str = fernet.decrypt(encrypted_data).decode()
        config = json.loads(decrypted_config_str)

        # Log the loaded product_key
        product_key = config.get('product_key')
        if not product_key:
            logger.error("Missing 'product_key' in the configuration.")
            raise ValueError("Product key is missing or invalid in configuration.")
        logger.info(f"Loaded product_key: {product_key}")

        return config
    except Exception as e:
        logger.error(f"Failed to load configuration from '{ox_file_path}': {e}")
        raise



# QuantumLDAPAuthenticator updated for product key
class QuantumLDAPAuthenticator:
    def __init__(self, key_vault_uri: str, product_key: str):
        if not isinstance(key_vault_uri, str):
            raise ValueError(f"key_vault_uri must be a string, got type '{type(key_vault_uri)}'")
        
        if not isinstance(product_key, str):
            raise ValueError(f"product_key must be a string, got type '{type(product_key)}'")

        """
        Initialize the QuantumLDAPAuthenticator with a Key Vault URI and product key.
        
        Parameters:
        - key_vault_uri (str): URI of the Azure Key Vault to retrieve secrets.
        - product_key (str): Product key for application configuration.
        """
        self.key_vault_uri = key_vault_uri
        self.product_key = product_key
        self.credential = self.get_credential()
        self.secret_client = SecretClient(vault_url=self.key_vault_uri, credential=self.credential)

    def get_credential(self):
        """
        Attempts to use DefaultAzureCredential for RBAC, falling back to ClientSecretCredential
        if a client ID and secret are provided.
        """
        client_id = os.getenv("AZURE_CLIENT_ID")
        client_secret = os.getenv("AZURE_CLIENT_SECRET")
        tenant_id = os.getenv("AZURE_TENANT_ID")

        if client_id and client_secret and tenant_id:
            logger.info("Using ClientSecretCredential for Key Vault access.")
            return ClientSecretCredential(client_id=client_id, client_secret=client_secret, tenant_id=tenant_id)
        
        logger.info("Using DefaultAzureCredential for Key Vault access.")
        return DefaultAzureCredential()

    def load_key(self, secret_name: str) -> str:
        """
        Retrieve a secret from Azure Key Vault with error handling.
        
        Parameters:
        - secret_name (str): The name of the secret to retrieve.

        Returns:
        - str: The value of the retrieved secret.
        """
        if not secret_name:
            raise ValueError("Secret name must be provided.")
        
        try:
            secret = self.secret_client.get_secret(secret_name)
            logger.info(f"Successfully retrieved secret: {secret_name}")
            return secret.value
        except ClientAuthenticationError as auth_error:
            logger.error(f"Authentication error: Ensure proper permissions for RBAC or Key Vault access policies. Details: {auth_error}")
            raise
        except HttpResponseError as e:
            if "AccessDenied" in str(e):
                logger.warning(f"Access denied to Key Vault secret '{secret_name}': {e}")
                raise ValueError("Insufficient permissions to access Key Vault. Check RBAC or Key Vault access policies.")
            else:
                logger.error(f"HTTP error retrieving secret '{secret_name}': {e}")
                raise
        except ResourceNotFoundError:
            logger.error(f"Secret '{secret_name}' not found in Key Vault at '{self.key_vault_uri}'.")
            raise
        except Exception as e:
            logger.exception(f"An unexpected error occurred while retrieving secret '{secret_name}': {e}")
            raise

# Usage example
if __name__ == "__main__":
    try:
        # Load Key Vault URI from the .ox file
        key_vault_uri = load_key_vault_uri()

        # Load product key from the .ox file
        product_key = load_product_key()

        # Debugging statement: check what the key_vault_uri and product_key are
        logger.debug(f"Retrieved key_vault_uri: {key_vault_uri} of type {type(key_vault_uri)}")
        logger.debug(f"Retrieved product_key: {product_key} of type {type(product_key)}")

        # Ensure key_vault_uri is a valid string
        if not isinstance(key_vault_uri, str) or not key_vault_uri:
            logger.error("Key Vault URI must be a string and is required in configuration.")
            raise ValueError(f"Key Vault URI must be a valid string, but got type '{type(key_vault_uri)}'.")

        # Initialize the authenticator with the Key Vault URI and product key
        authenticator = QuantumLDAPAuthenticator(key_vault_uri=key_vault_uri, product_key=product_key)
        logger.info("QuantumLDAPAuthenticator initialized successfully.")
    except ValueError as e:
        logger.error(f"Configuration error: {e}")
    except Exception as e:
        logger.error(f"Failed to initialize QuantumLDAPAuthenticator: {e}")
