import numpy as np
import logging
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
import os

# Initialize logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class DuoOctuplinearThreatHunter:
    def __init__(self, encryption_key):
        self.model = IsolationForest(contamination=0.05)  # Adjusted contamination for more corporate/military settings
        self.scaler = StandardScaler()
        self.encryption_key = encryption_key
        self.iv = os.urandom(16)  # Initialization vector for encryption

    def encrypt_data(self, data):
        """Encrypt data for secure handling."""
        try:
            cipher = Cipher(algorithms.AES(self.encryption_key), modes.CFB(self.iv))
            encryptor = cipher.encryptor()
            padded_data = padding.PKCS7(algorithms.AES.block_size).padder().update(data) + padding.PKCS7(algorithms.AES.block_size).padder().finalize()
            encrypted_data = encryptor.update(padded_data) + encryptor.finalize()
            return encrypted_data
        except Exception as e:
            logging.error(f"Error encrypting data: {e}")
            raise

    def decrypt_data(self, encrypted_data):
        """Decrypt data for analysis."""
        try:
            cipher = Cipher(algorithms.AES(self.encryption_key), modes.CFB(self.iv))
            decryptor = cipher.decryptor()
            padded_data = decryptor.update(encrypted_data) + decryptor.finalize()
            unpadded_data = padding.PKCS7(algorithms.AES.block_size).unpadder().update(padded_data) + padding.PKCS7(algorithms.AES.block_size).unpadder().finalize()
            return unpadded_data
        except Exception as e:
            logging.error(f"Error decrypting data: {e}")
            raise

    def train_model(self, data):
        """Train the threat detection model with encrypted data."""
        try:
            data = self.decrypt_data(data)
            scaled_data = self.scaler.fit_transform(data)
            self.model.fit(scaled_data)
            logging.info("Threat detection model trained successfully.")
        except Exception as e:
            logging.error(f"Error training model: {e}")
            raise

    def detect_threats(self, data):
        """Detect threats using the trained model on encrypted data."""
        try:
            data = self.decrypt_data(data)
            scaled_data = self.scaler.transform(data)
            predictions = self.model.predict(scaled_data)
            threats = predictions == -1  # -1 indicates an anomaly
            logging.info("Threat detection complete.")
            return threats
        except Exception as e:
            logging.error(f"Error detecting threats: {e}")
            raise

    def quarantine_threats(self, threats, data):
        """Quarantine detected threats."""
        try:
            quarantined_data = [data[i] for i in range(len(threats)) if threats[i]]
            logging.info(f"Quarantined {len(quarantined_data)} threats.")
            return quarantined_data
        except Exception as e:
            logging.error(f"Error quarantining threats: {e}")
            raise

    def evaluate_model(self, data, labels):
        """Evaluate the performance of the threat detection model."""
        try:
            scaled_data = self.scaler.transform(data)
            predictions = self.model.predict(scaled_data)
            predictions = [1 if p == -1 else 0 for p in predictions]  # Convert -1 to 1 (threat), 1 to 0 (normal)
            report = classification_report(labels, predictions)
            logging.info("Model evaluation complete.")
            logging.info(f"Classification Report:\n{report}")
            return report
        except Exception as e:
            logging.error(f"Error evaluating model: {e}")
            raise

# Example usage
if __name__ == "__main__":
    # Example data for demonstration purposes
    example_data = np.array([[1.0, 2.0], [1.1, 2.1], [10.0, 20.0], [10.1, 20.1]])  # Example data points
    example_labels = np.array([0, 0, 1, 1])  # Example labels: 0 for normal, 1 for threat

    encryption_key = os.urandom(32)  # Encryption key for secure data handling
    hunter = DuoOctuplinearThreatHunter(encryption_key)
    
    encrypted_data = hunter.encrypt_data(example_data)
    hunter.train_model(encrypted_data)
    threats = hunter.detect_threats(encrypted_data)
    quarantined_data = hunter.quarantine_threats(threats, example_data)
    report = hunter.evaluate_model(example_data, example_labels)