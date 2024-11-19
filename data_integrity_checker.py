import hashlib
import logging

class DataIntegrityChecker:
    def __init__(self):
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    def compute_hash(self, data):
        """Compute the SHA-256 hash of the given data."""
        if isinstance(data, str):
            data = data.encode('utf-8')  # Encode string data to bytes
        elif not isinstance(data, bytes):
            logging.error("Data must be a string or bytes.")
            raise ValueError("Data must be a string or bytes.")

        hash_value = hashlib.sha256(data).hexdigest()
        logging.info(f"Computed hash: {hash_value}")
        return hash_value

    def check_integrity(self, original_data, hash_value):
        """Check the integrity of data by comparing its computed hash to the given hash value."""
        computed_hash = self.compute_hash(original_data)
        integrity_status = computed_hash == hash_value

        if integrity_status:
            logging.info("Data integrity check passed.")
        else:
            logging.warning("Data integrity check failed!")

        return integrity_status

# Example usage:
if __name__ == "__main__":
    checker = DataIntegrityChecker()

    # Original data
    original_data = "Sensitive information."
    
    # Compute hash of the original data
    original_hash = checker.compute_hash(original_data)

    # Simulate data transmission or storage...
    # Check integrity of the original data
    checker.check_integrity(original_data, original_hash)

    # Simulate data corruption
    corrupted_data = "Corrupted information."
    
    # Check integrity of the corrupted data
    checker.check_integrity(corrupted_data, original_hash)
