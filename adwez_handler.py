from cryptography.fernet import Fernet
import zipfile
import logging
import os

class AQVPDeltaWaveEnhancedZIP:
    def __init__(self, secret_key):
        self.secret_key = secret_key
        self.cipher = Fernet(secret_key)
        logging.info("AQVP Delta Wave Enhanced ZIP initialized with encryption.")

    def compress_to_adwez(self, input_file, output_file):
        """Compresses data using AQVP Delta Wave Enhanced ZIP format and encrypts it."""
        logging.info(f"Compressing and encrypting {input_file} to {output_file}.")
        try:
            # Compress the file
            with zipfile.ZipFile(output_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
                zipf.write(input_file)
            logging.info(f"File {input_file} compressed successfully.")

            # Encrypt the compressed file
            with open(output_file, 'rb') as file:
                compressed_data = file.read()

            encrypted_data = self.cipher.encrypt(compressed_data)

            # Save the encrypted data
            with open(output_file, 'wb') as file:
                file.write(encrypted_data)
            logging.info(f"File {output_file} encrypted successfully.")

        except Exception as e:
            logging.error(f"Error during compression and encryption: {e}")

    def decompress_from_adwez(self, input_file, output_file):
        """Decrypts and decompresses AQVP Delta Wave Enhanced ZIP formatted files."""
        logging.info(f"Decrypting and decompressing {input_file} to {output_file}.")
        try:
            # Decrypt the encrypted file
            with open(input_file, 'rb') as file:
                encrypted_data = file.read()

            decrypted_data = self.cipher.decrypt(encrypted_data)

            # Save the decrypted data
            temp_decrypted_file = input_file + '.decrypted'
            with open(temp_decrypted_file, 'wb') as file:
                file.write(decrypted_data)

            # Decompress the decrypted file
            with zipfile.ZipFile(temp_decrypted_file, 'r') as zipf:
                zipf.extractall(output_file)
            logging.info(f"File {input_file} decrypted and decompressed successfully.")

            # Clean up the temporary decrypted file
            os.remove(temp_decrypted_file)

        except Exception as e:
            logging.error(f"Error during decryption and decompression: {e}")
