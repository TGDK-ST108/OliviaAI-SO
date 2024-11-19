import json
from cryptography.fernet import Fernet

# Load the key for decryption
def load_encryption_key(key_path='ox_key.key'):
    try:
        with open(key_path, 'rb') as key_file:
            key = key_file.read()
        logger.info("Encryption key loaded successfully.")
        return key
    except FileNotFoundError:
        logger.error(f"Encryption key file '{key_path}' not found.")
        raise

# Load configuration from an .ox file
def load_from_ox_file(ox_file_path='config.ox', key=None):
    try:
        if key is None:
            # Load key from file if not provided
            key = load_encryption_key()

        # Initialize Fernet with the key
        fernet = Fernet(key)

        # Read the encrypted configuration from the .ox file
        with open(ox_file_path, 'rb') as ox_file:
            encrypted_config = ox_file.read()

        # Decrypt the configuration string
        decrypted_config_str = fernet.decrypt(encrypted_config).decode()

        # Deserialize JSON string to dictionary
        config = json.loads(decrypted_config_str)
        logger.info(f"Configuration successfully loaded from '{ox_file_path}'.")
        return config
    except Exception as e:
        logger.error(f"Failed to load configuration from '{ox_file_path}': {e}")
        raise

if __name__ == "__main__":
    # Load configuration from .ox file
    config = load_from_ox_file()

    # Debug print configuration to verify it loads correctly
    logger.debug(json.dumps(config, indent=2))
