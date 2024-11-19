
import logging
import hashlib
from typing import Any

class ChecksumCartography:
    def __init__(self):
        logging.info("ChecksumCartography initialized.")

    def generate_checksum(self, data: Any, algorithm: str = 'sha256') -> str:
        logging.info("Generating checksum using %s algorithm.", algorithm)
        if isinstance(data, str):
            data_bytes = data.encode('utf-8')
        elif isinstance(data, bytes):
            data_bytes = data
        else:
            data_bytes = str(data).encode('utf-8')
        
        hash_func = hashlib.new(algorithm)
        hash_func.update(data_bytes)
        checksum = hash_func.hexdigest()
        logging.info("Generated checksum: %s", checksum)
        return checksum

    def verify_checksum(self, data: Any, checksum: str, algorithm: str = 'sha256') -> bool:
        logging.info("Verifying checksum.")
        generated_checksum = self.generate_checksum(data, algorithm)
        is_valid = generated_checksum == checksum
        if is_valid:
            logging.info("Checksum verification passed.")
        else:
            logging.warning("Checksum verification failed.")
        return is_valid
