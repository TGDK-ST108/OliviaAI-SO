import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes

class EncryptionManager:
    def __init__(self, key=None):
        self.key = key or self.generate_key()

    @staticmethod
    def generate_key():
        """Generates a new AES key."""
        return os.urandom(32)  # AES-256 key

    def encrypt(self, plaintext):
        """Encrypts the given plaintext using AES encryption."""
        iv = os.urandom(16)  # Generate a random initialization vector
        cipher = Cipher(algorithms.AES(self.key), modes.CBC(iv), backend=default_backend())
        encryptor = cipher.encryptor()

        # Pad plaintext to be a multiple of the block size
        padder = padding.PKCS7(algorithms.AES.block_size).padder()
        padded_data = padder.update(plaintext.encode()) + padder.finalize()

        ciphertext = encryptor.update(padded_data) + encryptor.finalize()
        return iv + ciphertext  # Prepend IV for use in decryption

    def decrypt(self, ciphertext):
        """Decrypts the given ciphertext using AES decryption."""
        iv = ciphertext[:16]  # Extract the IV from the beginning
        actual_ciphertext = ciphertext[16:]

        cipher = Cipher(algorithms.AES(self.key), modes.CBC(iv), backend=default_backend())
        decryptor = cipher.decryptor()

        padded_data = decryptor.update(actual_ciphertext) + decryptor.finalize()

        # Unpad the plaintext
        unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
        plaintext = unpadder.update(padded_data) + unpadder.finalize()
        return plaintext.decode()

# Example usage:
if __name__ == "__main__":
    manager = EncryptionManager()
    secret_message = "This is a secret message."
    encrypted = manager.encrypt(secret_message)
    print("Encrypted:", encrypted)

    decrypted = manager.decrypt(encrypted)
    print("Decrypted:", decrypted)
