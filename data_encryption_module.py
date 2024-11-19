# data_encryption_module.py

from cryptography.fernet import Fernet
import logging

class EncryptionManager:
    def __init__(self, key: bytes = None):
        """
        Initialize the Encryption Manager.

        :param key: Encryption key. If None, a new key is generated.
        """
        if key is None:
            key = Fernet.generate_key()
            logging.info("Generated new encryption key.")
        self.fernet = Fernet(key)
        self.key = key

    def encrypt(self, data: bytes) -> bytes:
        """
        Encrypt data.

        :param data: Data to encrypt in bytes.
        :return: Encrypted data.
        """
        logging.info("Starting data encryption.")
        encrypted = self.fernet.encrypt(data)
        logging.info("Data encryption completed.")
        return encrypted

    def decrypt(self, encrypted_data: bytes) -> bytes:
        """
        Decrypt data.

        :param encrypted_data: Encrypted data in bytes.
        :return: Decrypted data.
        """
        logging.info("Starting data decryption.")
        decrypted = self.fernet.decrypt(encrypted_data)
        logging.info("Data decryption completed.")
        return decrypted

    def get_key(self) -> bytes:
        """
        Get the encryption key.

        :return: Encryption key in bytes.
        """
        return self.key
