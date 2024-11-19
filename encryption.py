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
        """Encrypts the given plaintext using QVP encryption."""
        return self.qvp_encrypt(plaintext)

    def decrypt(self, ciphertext):
        """Decrypts the given ciphertext using QVP decryption."""
        return self.qvp_decrypt(ciphertext)

    def aes_encrypt(self, plaintext):
        """Encrypts the given plaintext using AES encryption."""
        iv = os.urandom(16)  # Generate a random initialization vector
        cipher = Cipher(algorithms.AES(self.key), modes.CBC(iv), backend=default_backend())
        encryptor = cipher.encryptor()

        # Pad plaintext to be a multiple of the block size
        padder = padding.PKCS7(algorithms.AES.block_size).padder()
        padded_data = padder.update(plaintext.encode()) + padder.finalize()

        ciphertext = encryptor.update(padded_data) + encryptor.finalize()
        return iv + ciphertext  # Prepend IV for use in decryption

    def aes_decrypt(self, ciphertext):
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

    @staticmethod
    def xor_encrypt(plaintext, key):
        """Encrypts the plaintext using XOR encryption."""
        if len(key) < len(plaintext):
            raise ValueError("Key must be at least as long as the plaintext.")
        return bytes([p ^ k for p, k in zip(plaintext.encode(), key[:len(plaintext)])])

    @staticmethod
    def xor_decrypt(ciphertext, key):
        """Decrypts the ciphertext using XOR encryption."""
        if len(key) < len(ciphertext):
            raise ValueError("Key must be at least as long as the ciphertext.")
        return ''.join(chr(c ^ k) for c, k in zip(ciphertext, key[:len(ciphertext)]))

    def qvp_encrypt(self, plaintext):
        """Encrypts the plaintext using QVP encryption."""
        key_hash = hashes.Hash(hashes.SHA256(), backend=default_backend())
        key_hash.update(self.key)
        hashed_key = key_hash.finalize()

        return bytes([p ^ hashed_key[i % len(hashed_key)] for i, p in enumerate(plaintext.encode())])

    def qvp_decrypt(self, ciphertext):
        """Decrypts the ciphertext using QVP encryption."""
        key_hash = hashes.Hash(hashes.SHA256(), backend=default_backend())
        key_hash.update(self.key)
        hashed_key = key_hash.finalize()

        return ''.join(chr(c ^ hashed_key[i % len(hashed_key)]) for i, c in enumerate(ciphertext))

# Example usage:
if __name__ == "__main__":
    manager = EncryptionManager()

    # QVP encryption
    secret_message = "This is a secret message."
    qvp_encrypted = manager.encrypt(secret_message)
    print("QVP Encrypted:", qvp_encrypted)

    qvp_decrypted = manager.decrypt(qvp_encrypted)
    print("QVP Decrypted:", qvp_decrypted)

    # AES encryption
    aes_encrypted = manager.aes_encrypt(secret_message)
    print("AES Encrypted:", aes_encrypted)

    aes_decrypted = manager.aes_decrypt(aes_encrypted)
    print("AES Decrypted:", aes_decrypted)

    # XOR encryption
    xor_key = os.urandom(len(secret_message))  # Key must be at least as long as the plaintext
    xor_encrypted = manager.xor_encrypt(secret_message, xor_key)
    print("XOR Encrypted:", xor_encrypted)

    xor_decrypted = manager.xor_decrypt(xor_encrypted, xor_key)
    print("XOR Decrypted:", xor_decrypted)
