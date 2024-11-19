
import logging
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding as sym_padding
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers.aead import AESGCM, AESCCM, AESSIV
import os

# Configure logging for this module
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class EncryptionManager:
    def __init__(self, aes_key: bytes, xor_key: bytes, qvp_key: bytes, aqvp_key: bytes, deltatrilineation_key: bytes):
        """
        Initialize the EncryptionManager with keys for different encryption methods.

        :param aes_key: 32-byte key for AES-256.
        :param xor_key: Key for XOR encryption.
        :param qvp_key: Key for QVP encryption (mapped to AES-CTR).
        :param aqvp_key: Key for AQVP encryption (mapped to AES-GCM).
        :param deltatrilineation_key: Key for Deltatrilineation encryption (mapped to AES-EAX).
        """
        self.aes_key = aes_key
        self.xor_key = xor_key
        self.qvp_key = qvp_key
        self.aqvp_key = aqvp_key
        self.deltatrilineation_key = deltatrilineation_key
        self.backend = default_backend()
        logging.info("EncryptionManager initialized with provided keys.")

    # ----------------------- AES Encryption ----------------------- #

    def aes_encrypt(self, plaintext: str) -> bytes:
        """
        Encrypt plaintext using AES-256 in CBC mode.

        :param plaintext: The data to encrypt.
        :return: Encrypted data with IV prepended.
        """
        logging.info("Starting AES encryption.")
        iv = os.urandom(16)  # AES block size is 16 bytes
        cipher = Cipher(algorithms.AES(self.aes_key), modes.CBC(iv), backend=self.backend)
        encryptor = cipher.encryptor()
        padder = sym_padding.PKCS7(128).padder()
        padded_data = padder.update(plaintext.encode('utf-8')) + padder.finalize()
        ciphertext = encryptor.update(padded_data) + encryptor.finalize()
        encrypted_data = iv + ciphertext  # Prepend IV for use in decryption
        logging.info("AES encryption completed.")
        return encrypted_data

    def aes_decrypt(self, ciphertext: bytes) -> str:
        """
        Decrypt ciphertext using AES-256 in CBC mode.

        :param ciphertext: Encrypted data with IV prepended.
        :return: Decrypted plaintext.
        """
        logging.info("Starting AES decryption.")
        iv = ciphertext[:16]
        actual_ciphertext = ciphertext[16:]
        cipher = Cipher(algorithms.AES(self.aes_key), modes.CBC(iv), backend=self.backend)
        decryptor = cipher.decryptor()
        padded_plaintext = decryptor.update(actual_ciphertext) + decryptor.finalize()
        unpadder = sym_padding.PKCS7(128).unpadder()
        plaintext = unpadder.update(padded_plaintext) + unpadder.finalize()
        decrypted_data = plaintext.decode('utf-8')
        logging.info("AES decryption completed.")
        return decrypted_data

    # ----------------------- XOR Encryption ----------------------- #

    def xor_encrypt(self, plaintext: str) -> bytes:
        """
        Encrypt plaintext using XOR cipher.

        :param plaintext: The data to encrypt.
        :return: Encrypted data as bytes.
        """
        logging.info("Starting XOR encryption.")
        plaintext_bytes = plaintext.encode('utf-8')
        encrypted_bytes = bytes([b ^ self.xor_key[i % len(self.xor_key)] for i, b in enumerate(plaintext_bytes)])
        logging.info("XOR encryption completed.")
        return encrypted_bytes

    def xor_decrypt(self, ciphertext: bytes) -> str:
        """
        Decrypt ciphertext using XOR cipher.

        :param ciphertext: Encrypted data as bytes.
        :return: Decrypted plaintext.
        """
        logging.info("Starting XOR decryption.")
        decrypted_bytes = bytes([b ^ self.xor_key[i % len(self.xor_key)] for i, b in enumerate(ciphertext)])
        decrypted_data = decrypted_bytes.decode('utf-8')
        logging.info("XOR decryption completed.")
        return decrypted_data

    # ----------------------- QVP Encryption (AES-CTR) ----------------------- #

    def qvp_encrypt(self, plaintext: str) -> bytes:
        """
        Encrypt plaintext using QVP (Quantum Variable Protocol) mapped to AES-CTR mode.

        :param plaintext: The data to encrypt.
        :return: Encrypted data with nonce prepended.
        """
        logging.info("Starting QVP encryption (AES-CTR).")
        nonce = os.urandom(16)  # Recommended nonce size for AES-CTR
        cipher = Cipher(algorithms.AES(self.qvp_key), modes.CTR(nonce), backend=self.backend)
        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(plaintext.encode('utf-8')) + encryptor.finalize()
        encrypted_data = nonce + ciphertext  # Prepend nonce for use in decryption
        logging.info("QVP encryption (AES-CTR) completed.")
        return encrypted_data

    def qvp_decrypt(self, ciphertext: bytes) -> str:
        """
        Decrypt ciphertext using QVP (Quantum Variable Protocol) mapped to AES-CTR mode.

        :param ciphertext: Encrypted data with nonce prepended.
        :return: Decrypted plaintext.
        """
        logging.info("Starting QVP decryption (AES-CTR).")
        nonce = ciphertext[:16]
        actual_ciphertext = ciphertext[16:]
        cipher = Cipher(algorithms.AES(self.qvp_key), modes.CTR(nonce), backend=self.backend)
        decryptor = cipher.decryptor()
        plaintext = decryptor.update(actual_ciphertext) + decryptor.finalize()
        decrypted_data = plaintext.decode('utf-8')
        logging.info("QVP decryption (AES-CTR) completed.")
        return decrypted_data

    # ----------------------- AQVP Encryption (AES-GCM) ----------------------- #

    def aqvp_encrypt(self, plaintext: str) -> bytes:
        """
        Encrypt plaintext using AQVP (Advanced Quantum Variable Protocol) mapped to AES-GCM mode.

        :param plaintext: The data to encrypt.
        :return: Encrypted data with nonce prepended.
        """
        logging.info("Starting AQVP encryption (AES-GCM).")
        nonce = os.urandom(12)  # Recommended nonce size for AES-GCM
        aesgcm = AESGCM(self.aqvp_key)
        ciphertext = aesgcm.encrypt(nonce, plaintext.encode('utf-8'), None)
        encrypted_data = nonce + ciphertext  # Prepend nonce for use in decryption
        logging.info("AQVP encryption (AES-GCM) completed.")
        return encrypted_data

    def aqvp_decrypt(self, ciphertext: bytes) -> str:
        """
        Decrypt ciphertext using AQVP (Advanced Quantum Variable Protocol) mapped to AES-GCM mode.

        :param ciphertext: Encrypted data with nonce prepended.
        :return: Decrypted plaintext.
        """
        logging.info("Starting AQVP decryption (AES-GCM).")
        nonce = ciphertext[:12]
        actual_ciphertext = ciphertext[12:]
        aesgcm = AESGCM(self.aqvp_key)
        plaintext = aesgcm.decrypt(nonce, actual_ciphertext, None)
        decrypted_data = plaintext.decode('utf-8')
        logging.info("AQVP decryption (AES-GCM) completed.")
        return decrypted_data

    # ----------------------- Deltatrilineation Encryption (AES-EAX) ----------------------- #

    def deltatrilineation_encrypt(self, plaintext: str) -> bytes:
        """
        Encrypt plaintext using Deltatrilineation mapped to AES-EAX mode.

        :param plaintext: The data to encrypt.
        :return: Encrypted data with nonce prepended.
        """
        logging.info("Starting Deltatrilineation encryption (AES-EAX).")
        nonce = os.urandom(16)  # Recommended nonce size for AES-EAX
        cipher = Cipher(algorithms.AES(self.deltatrilineation_key), modes.EAX(nonce), backend=self.backend)
        encryptor = cipher.encryptor()
        ciphertext, tag = encryptor.update(plaintext.encode('utf-8')) + encryptor.finalize_with_tag()
        encrypted_data = nonce + tag + ciphertext  # Prepend nonce and tag for use in decryption
        logging.info("Deltatrilineation encryption (AES-EAX) completed.")
        return encrypted_data

    def deltatrilineation_decrypt(self, ciphertext: bytes) -> str:
        """
        Decrypt ciphertext using Deltatrilineation mapped to AES-EAX mode.

        :param ciphertext: Encrypted data with nonce and tag prepended.
        :return: Decrypted plaintext.
        """
        logging.info("Starting Deltatrilineation decryption (AES-EAX).")
        nonce = ciphertext[:16]
        tag = ciphertext[16:32]
        actual_ciphertext = ciphertext[32:]
        cipher = Cipher(algorithms.AES(self.deltatrilineation_key), modes.EAX(nonce), backend=self.backend)
        decryptor = cipher.decryptor()
        decryptor.authenticate_additional_data(None)
        try:
            plaintext = decryptor.update(actual_ciphertext) + decryptor.finalize_with_tag(tag)
            decrypted_data = plaintext.decode('utf-8')
            logging.info("Deltatrilineation decryption (AES-EAX) completed successfully.")
            return decrypted_data
        except Exception as e:
            logging.error(f"Deltatrilineation decryption failed: {e}")
            raise ValueError("Invalid ciphertext or key for Deltatrilineation decryption.")

    # ----------------------- Combined Encryption ----------------------- #

    def encrypt(self, plaintext: str, method: str = 'AES') -> bytes:
        """
        Encrypt plaintext using the specified method.

        :param plaintext: The data to encrypt.
        :param method: The encryption method ('AES', 'XOR', 'QVP', 'AQVP', 'Deltatrilineation').
        :return: Encrypted data as bytes.
        """
        logging.info(f"Encrypting data using {method} method.")
        if method.upper() == 'AES':
            return self.aes_encrypt(plaintext)
        elif method.upper() == 'XOR':
            return self.xor_encrypt(plaintext)
        elif method.upper() == 'QVP':
            return self.qvp_encrypt(plaintext)
        elif method.upper() == 'AQVP':
            return self.aqvp_encrypt(plaintext)
        elif method.upper() == 'DELTATRILINEATION':
            return self.deltatrilineation_encrypt(plaintext)
        else:
            logging.error(f"Unsupported encryption method: {method}")
            raise ValueError(f"Unsupported encryption method: {method}")

    def decrypt(self, ciphertext: bytes, method: str = 'AES') -> str:
        """
        Decrypt ciphertext using the specified method.

        :param ciphertext: Encrypted data as bytes.
        :param method: The decryption method ('AES', 'XOR', 'QVP', 'AQVP', 'Deltatrilineation').
        :return: Decrypted plaintext.
        """
        logging.info(f"Decrypting data using {method} method.")
        if method.upper() == 'AES':
            return self.aes_decrypt(ciphertext)
        elif method.upper() == 'XOR':
            return self.xor_decrypt(ciphertext)
        elif method.upper() == 'QVP':
            return self.qvp_decrypt(ciphertext)
        elif method.upper() == 'AQVP':
            return self.aqvp_decrypt(ciphertext)
        elif method.upper() == 'DELTATRILINEATION':
            return self.deltatrilineation_decrypt(ciphertext)
        else:
            logging.error(f"Unsupported decryption method: {method}")
            raise ValueError(f"Unsupported decryption method: {method}")


# ----------------------- Example Usage ----------------------- #

if __name__ == "__main__":
    # Example keys (in practice, use secure key management)
    AES_KEY = os.urandom(32)  # 256-bit key for AES
    XOR_KEY = b'secretkey123'  # Simple XOR key (should be random and secure)
    QVP_KEY = os.urandom(32)  # 256-bit key for QVP (AES-CTR)
    AQVP_KEY = os.urandom(32)  # 256-bit key for AQVP (AES-GCM)
    DELTATRILINEATION_KEY = os.urandom(32)  # 256-bit key for Deltatrilineation (AES-EAX)

    # Initialize EncryptionManager
    enc_manager = EncryptionManager(
        aes_key=AES_KEY,
        xor_key=XOR_KEY,
        qvp_key=QVP_KEY,
        aqvp_key=AQVP_KEY,
        deltatrilineation_key=DELTATRILINEATION_KEY
    )

    # Sample plaintext
    plaintext = "Confidential Data"

    # AES Encryption
    aes_encrypted = enc_manager.encrypt(plaintext, method='AES')
    print("AES Encrypted:", aes_encrypted)
    aes_decrypted = enc_manager.decrypt(aes_encrypted, method='AES')
    print("AES Decrypted:", aes_decrypted)

    # XOR Encryption
    xor_encrypted = enc_manager.encrypt(plaintext, method='XOR')
    print("XOR Encrypted:", xor_encrypted)
    xor_decrypted = enc_manager.decrypt(xor_encrypted, method='XOR')
    print("XOR Decrypted:", xor_decrypted)

    # QVP Encryption (AES-CTR)
    qvp_encrypted = enc_manager.encrypt(plaintext, method='QVP')
    print("QVP Encrypted (AES-CTR):", qvp_encrypted)
    qvp_decrypted = enc_manager.decrypt(qvp_encrypted, method='QVP')
    print("QVP Decrypted (AES-CTR):", qvp_decrypted)

    # AQVP Encryption (AES-GCM)
    aqvp_encrypted = enc_manager.encrypt(plaintext, method='AQVP')
    print("AQVP Encrypted (AES-GCM):", aqvp_encrypted)
    aqvp_decrypted = enc_manager.decrypt(aqvp_encrypted, method='AQVP')
    print("AQVP Decrypted (AES-GCM):", aqvp_decrypted)

    # Deltatrilineation Encryption (AES-EAX)
    delt_encrypted = enc_manager.encrypt(plaintext, method='Deltatrilineation')
    print("Deltatrilineation Encrypted (AES-EAX):", delt_encrypted)
    delt_decrypted = enc_manager.decrypt(delt_encrypted, method='Deltatrilineation')
    print("Deltatrilineation Decrypted (AES-EAX):", delt_decrypted)
