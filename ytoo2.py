import os
import getpass
import json
from cryptography.fernet import Fernet

# File paths
OX_FILE_PATH = 'key_vault.ox'
KEY_FILE_PATH = 'ox_key.key'

# Generate or load encryption key
def load_or_create_key():
    """
    Loads an existing encryption key or generates a new one.
    """
    if os.path.exists(KEY_FILE_PATH):
        with open(KEY_FILE_PATH, 'rb') as key_file:
            key = key_file.read()
    else:
        key = Fernet.generate_key()
        with open(KEY_FILE_PATH, 'wb') as key_file:
            key_file.write(key)
    return key

# Create a Key Vault file
def create_ox_key_vault_file():
    """
    Prompts the user for Key Vault URI and stores it securely in an encrypted .ox file.
    """
    # Load or create the encryption key
    key = load_or_create_key()
    fernet = Fernet(key)

    # Get the Key Vault URI from the user
    key_vault_uri = getpass.getpass("Enter Key Vault URI: ")
    if not key_vault_uri:
        print("Key Vault URI cannot be empty.")
        return

    # Create dictionary to store the URI
    key_vault_data = {
        "key_vault_uri": key_vault_uri
    }

    # Convert data to JSON and encrypt
    data_json = json.dumps(key_vault_data).encode('utf-8')
    encrypted_data = fernet.encrypt(data_json)

    # Save encrypted data to .ox file
    with open(OX_FILE_PATH, 'wb') as ox_file:
        ox_file.write(encrypted_data)

    print(f"Key Vault URI successfully stored in '{OX_FILE_PATH}'.")

# Load the Key Vault URI from the .ox file
def load_ox_key_vault_file():
    """
    Loads and decrypts the Key Vault URI from the .ox file.
    """
    # Load the encryption key
    if not os.path.exists(KEY_FILE_PATH):
        raise FileNotFoundError("Encryption key file not found. Please create the .ox file first.")
    with open(KEY_FILE_PATH, 'rb') as key_file:
        key = key_file.read()
    fernet = Fernet(key)

    # Load and decrypt the .ox file
    if not os.path.exists(OX_FILE_PATH):
        raise FileNotFoundError("Key Vault .ox file not found. Please create it first.")
    with open(OX_FILE_PATH, 'rb') as ox_file:
        encrypted_data = ox_file.read()

    decrypted_data = fernet.decrypt(encrypted_data)
    key_vault_data = json.loads(decrypted_data.decode('utf-8'))
    return key_vault_data["key_vault_uri"]

if __name__ == "__main__":
    # Create the .ox file with the Key Vault URI
    create_ox_key_vault_file()

    # Example usage: Load the Key Vault URI
    try:
        uri = load_ox_key_vault_file()
        print(f"Loaded Key Vault URI: {uri}")
    except FileNotFoundError as e:
        print(e)
