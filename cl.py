import os
import logging
from cryptography.fernet import Fernet
import yaml

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Generate or load the encryption key
def load_or_create_encryption_key(key_path='config/ox_key.key'):
    """
    Generate or load an encryption key from a specified file.
    """
    if not os.path.exists(key_path):
        # Generate a new key if it doesn't exist
        key = Fernet.generate_key()
        os.makedirs(os.path.dirname(key_path), exist_ok=True)
        with open(key_path, 'wb') as key_file:
            key_file.write(key)
        logger.info(f"Encryption key generated and saved to '{key_path}'.")
    else:
        # Load the existing key
        with open(key_path, 'rb') as key_file:
            key = key_file.read()
        logger.info(f"Encryption key loaded from '{key_path}'.")
    return key

# Encrypt a YAML file and save it as an .ox file
def encrypt_yaml_to_ox(input_yaml_path, output_ox_path='config/config.ox', key_path='config/ox_key.key'):
    """
    Encrypt an existing YAML file and save it as an .ox file.
    
    Args:
        input_yaml_path (str): Path to the input YAML file to encrypt.
        output_ox_path (str): Path to save the encrypted .ox file.
        key_path (str): Path to the encryption key.
    """
    # Load or create the encryption key
    key = load_or_create_encryption_key(key_path)
    fernet = Fernet(key)

    # Load the YAML file
    if not os.path.exists(input_yaml_path):
        raise FileNotFoundError(f"Input YAML file '{input_yaml_path}' not found.")

    with open(input_yaml_path, 'r') as yaml_file:
        yaml_data = yaml_file.read()

    # Encrypt the YAML data
    encrypted_data = fernet.encrypt(yaml_data.encode())

    # Save the encrypted data to an .ox file
    os.makedirs(os.path.dirname(output_ox_path), exist_ok=True)
    with open(output_ox_path, 'wb') as ox_file:
        ox_file.write(encrypted_data)

    logger.info(f"YAML file encrypted and saved as .ox file to '{output_ox_path}'.")

# Decrypt an .ox file and return its YAML content
def decrypt_ox_to_yaml(ox_file_path, key_path='config/ox_key.key'):
    """
    Decrypt an .ox file and return its content as a dictionary.
    
    Args:
        ox_file_path (str): Path to the encrypted .ox file.
        key_path (str): Path to the encryption key.

    Returns:
        dict: Decrypted YAML content.
    """
    # Load the encryption key
    key = load_or_create_encryption_key(key_path)
    fernet = Fernet(key)

    # Load the encrypted .ox file
    if not os.path.exists(ox_file_path):
        raise FileNotFoundError(f"Encrypted .ox file '{ox_file_path}' not found.")

    with open(ox_file_path, 'rb') as ox_file:
        encrypted_data = ox_file.read()

    # Decrypt the YAML data
    decrypted_data = fernet.decrypt(encrypted_data).decode()

    # Parse the YAML data into a dictionary
    config = yaml.safe_load(decrypted_data)
    logger.info("Encrypted .ox file decrypted successfully.")
    return config

# Main script
if __name__ == "__main__":
    try:
        # Specify paths
        input_yaml_path = input("Enter the path to the YAML file you want to encrypt: ").strip()
        output_ox_path = 'config/config.ox'
        key_path = 'config/ox_key.key'

        # Encrypt the YAML file to an .ox file
        encrypt_yaml_to_ox(input_yaml_path, output_ox_path, key_path)

        # Optionally decrypt and verify the result
        logger.info("Decrypting the .ox file for verification...")
        decrypted_config = decrypt_ox_to_yaml(output_ox_path, key_path)
        logger.info(f"Decrypted configuration: {decrypted_config}")

    except Exception as e:
        logger.error(f"An error occurred: {e}")
