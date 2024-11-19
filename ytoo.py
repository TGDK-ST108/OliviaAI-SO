import os
import yaml
import json
import base64
import logging
from cryptography.fernet import Fernet

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load the YAML configuration
def load_yaml_config(config_path='config.yaml'):
    try:
        with open(config_path, 'r') as file:
            config = yaml.safe_load(file)
        logger.info("YAML configuration loaded successfully.")
        return config
    except FileNotFoundError:
        logger.error(f"Configuration file '{config_path}' not found.")
        raise
    except yaml.YAMLError as e:
        logger.error(f"Error parsing YAML file: {e}")
        raise

# Encrypt and save configuration to an .ox file
def save_to_ox_file(config, ox_file_path='config.ox', key=None):
    try:
        if key is None:
            # Generate a key for encryption (store this securely)
            key = Fernet.generate_key()
            with open("ox_key.key", 'wb') as key_file:
                key_file.write(key)
            logger.info("Encryption key generated and saved to 'ox_key.key'.")

        # Initialize Fernet with the key
        fernet = Fernet(key)

        # Serialize configuration to JSON string
        config_str = json.dumps(config)

        # Encrypt the configuration string
        encrypted_config = fernet.encrypt(config_str.encode())

        # Save the encrypted configuration to the .ox file
        with open(ox_file_path, 'wb') as ox_file:
            ox_file.write(encrypted_config)

        logger.info(f"Configuration successfully saved to '{ox_file_path}'.")
    except Exception as e:
        logger.error(f"Failed to save configuration to '{ox_file_path}': {e}")
        raise

if __name__ == "__main__":
    # Load YAML configuration
    config = load_yaml_config()

    # Encrypt and save configuration to .ox file
    save_to_ox_file(config)
