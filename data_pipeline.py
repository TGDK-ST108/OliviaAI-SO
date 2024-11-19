import logging
import os
import numpy as np
import pandas as pd
from cryptography.fernet import Fernet
from data_validator import DataValidator
from feature_engineer import FeatureEngineer
from anomaly_detector import AnomalyDetector
from data_encryption_module import EncryptionManager
from storage_manager import StorageManager

class DataPipeline:
    def __init__(self, log_level=logging.INFO, encryption_key=None):
        # Set up logging configuration
        logging.basicConfig(level=log_level, format='%(asctime)s - %(levelname)s - %(message)s')
        
        self.logger = logging.getLogger("DataPipeline")
        self.validator = DataValidator()
        self.feature_engineer = FeatureEngineer()
        self.anomaly_detector = AnomalyDetector()
        
        # Use a provided encryption key or generate a new one
        self.encryption_key = encryption_key or Fernet.generate_key()
        self.encryption_manager = EncryptionManager(self.encryption_key)
        
        self.storage_manager = StorageManager()
        self.data = None

    def ingest_data(self, source):
        """Ingest data from a specified source (e.g., DataFrame, file path, or API)."""
        try:
            if isinstance(source, pd.DataFrame):
                self.data = source
            elif isinstance(source, str) and os.path.isfile(source):  # Assume file path
                if source.endswith('.csv'):
                    self.data = pd.read_csv(source)
                elif source.endswith('.json'):
                    self.data = pd.read_json(source)
                else:
                    raise ValueError("Unsupported file format.")
            else:
                raise ValueError("Unsupported data source format.")
            self.logger.info("Data ingestion completed.")
        except Exception as e:
            self.logger.error(f"Error during data ingestion: {e}")
            raise

    def validate_data(self):
        """Run data through validation checks."""
        try:
            if not self.validator.validate(self.data):
                raise ValueError("Data validation failed.")
            self.logger.info("Data validation passed.")
        except Exception as e:
            self.logger.error(f"Error during data validation: {e}")
            raise

    def transform_data(self):
        """Transform and preprocess data (e.g., feature engineering)."""
        try:
            self.data = self.feature_engineer.generate_features(self.data)
            self.logger.info("Data transformation and feature engineering completed.")
        except Exception as e:
            self.logger.error(f"Error during data transformation: {e}")
            raise

    def detect_anomalies(self):
        """Detect anomalies in data."""
        try:
            anomalies = self.anomaly_detector.detect(self.data)
            if anomalies:
                self.logger.warning(f"Anomalies detected: {anomalies}")
            return anomalies
        except Exception as e:
            self.logger.error(f"Error during anomaly detection: {e}")
            raise

    def encrypt_data(self):
        """Encrypt data to secure sensitive information."""
        try:
            encrypted_data = self.encryption_manager.encrypt(self.data.to_json().encode())
            self.logger.info("Data encryption completed.")
            return encrypted_data
        except Exception as e:
            self.logger.error(f"Error during data encryption: {e}")
            raise

    def store_data(self, encrypted_data):
        """Store encrypted data securely."""
        try:
            self.storage_manager.store(encrypted_data)
            self.logger.info("Encrypted data stored successfully.")
        except Exception as e:
            self.logger.error(f"Error during data storage: {e}")
            raise

    def run_pipeline(self, source):
        """Run the full data pipeline."""
        try:
            self.ingest_data(source)
            self.validate_data()
            self.transform_data()
            anomalies = self.detect_anomalies()
            encrypted_data = self.encrypt_data()
            self.store_data(encrypted_data)
            return {"status": "Pipeline completed successfully", "anomalies": anomalies}
        except Exception as e:
            self.logger.error(f"Error running data pipeline: {e}")
            raise

# Example usage
if __name__ == "__main__":
    # Mock data example
    data = pd.DataFrame({
        'sensor_value': np.random.randn(100),
        'timestamp': pd.date_range(start='2023-01-01', periods=100, freq='H')
    })
    
    # Initialize the DataPipeline with DEBUG level logging and a persistent encryption key
    encryption_key = Fernet.generate_key()  # Or load from a secure location
    pipeline = DataPipeline(log_level=logging.DEBUG, encryption_key=encryption_key)
    
    # Run the pipeline with the mock data
    result = pipeline.run_pipeline(data)
    print("Pipeline Result:", result)
