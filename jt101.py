import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.hashes import SHA256
import base64
import json


class HFTM:
    def __init__(self, encrypted_file: str, key_file: str):
        self.encrypted_file = encrypted_file
        self.key_file = key_file

    def _load_key(self):
        """Load the key from the key file."""
        try:
            with open(self.key_file, 'rb') as key_f:
                key_data = key_f.read()
                return base64.urlsafe_b64decode(key_data)
        except Exception as e:
            raise ValueError(f"Failed to load the key file: {e}")

    def _decrypt_file(self, key):
        """Decrypt the encrypted file using the provided key."""
        try:
            with open(self.encrypted_file, 'rb') as enc_f:
                file_data = enc_f.read()

            # Extract IV and ciphertext from the encrypted file
            iv = file_data[:16]
            ciphertext = file_data[16:]

            # Decrypt the data
            cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
            decryptor = cipher.decryptor()
            plaintext = decryptor.update(ciphertext) + decryptor.finalize()

            return plaintext
        except Exception as e:
            raise ValueError(f"Failed to decrypt the file: {e}")

    def get_token(self):
        """Retrieve the Hugging Face token from the encrypted file."""
        try:
            key = self._load_key()
            decrypted_data = self._decrypt_file(key)
            
            # Parse the decrypted JSON to extract the token
            token_data = json.loads(decrypted_data.decode('utf-8'))
            return token_data.get('hugging_face_token')
        except Exception as e:
            raise ValueError(f"Failed to retrieve the token: {e}")

    def pass_token_to_process(self, process_function):
        """Pass the Hugging Face token to another process."""
        try:
            token = self.get_token()
            process_function(token)
        except Exception as e:
            raise ValueError(f"Failed to pass the token to the process: {e}")

from transformers import AutoTokenizer, AutoModelForSequenceClassification

# Example usage of HFTM
if __name__ == "__main__":
    # File paths for the encrypted file and key file
    encrypted_file = "j1.ox"
    key_file = "m1.key"

    # Initialize the token manager
    manager = HFTM(encrypted_file=encrypted_file, key_file=key_file)

    # Retrieve the Hugging Face token
    try:
        hugging_face_token = manager.get_token()
        print("Token retrieved successfully.")

        # Define model name
        model_name = "OliviaAI"  # Replace with your desired model

        # Load tokenizer and model with the token
        tokenizer = AutoTokenizer.from_pretrained(model_name, use_auth_token=hugging_face_token)
        model = AutoModelForSequenceClassification.from_pretrained(model_name, use_auth_token=hugging_face_token)

        # Example processing with tokenizer and model
        snippet = "def add(a, b): return a + b"
        tokenized = tokenizer(snippet, return_tensors="pt", truncation=True, padding="max_length")
        print("Tokenized Output:", tokenized)
    except Exception as e:
        print(f"Error: {e}")
