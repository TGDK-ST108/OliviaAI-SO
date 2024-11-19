import os
import sys
import logging
import hashlib
import json
import yaml
import ast
import re
import pandas as pd
import numpy as np
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
from cryptography.fernet import Fernet
from quantum_sdk_toolkit import QuantumFeatureMapper  # Assuming this is a valid module in the toolkit


# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def map_code_to_quantum_features(name):
    """
    Map a function name to quantum features using Quantum_sdk_toolkit.
    
    Args:
        name (str): The function name to map.
    
    Returns:
        dict: A dictionary of quantum-derived features.
    """
    if pd.isna(name) or not isinstance(name, str):
        return {"quantum_hash": None, "distribution_pattern": None, "entangled_features": None}
    
    try:
        # Initialize QuantumFeatureMapper with required arguments
        qfm = QuantumFeatureMapper(provider="IBM", num_qubits=5)
        
        # Generate quantum features
        quantum_hash = qfm.generate_hash(name)
        quantum_distribution = qfm.compute_distribution(name)
        entangled_features = qfm.generate_entanglement(name)
        
        return {
            "quantum_hash": quantum_hash,
            "distribution_pattern": quantum_distribution,
            "entangled_features": entangled_features
        }
    except Exception as e:
        print(f"Error generating quantum features for {name}: {e}")
        return {"quantum_hash": None, "distribution_pattern": None, "entangled_features": None}

# Encryption and Decryption Utilities
class SecureFileManager:
    @staticmethod
    def load_or_create_key(key_path='config/ox_key.key'):
        """Generate or load encryption key."""
        if not os.path.exists(key_path):
            key = Fernet.generate_key()
            os.makedirs(os.path.dirname(key_path), exist_ok=True)
            with open(key_path, 'wb') as key_file:
                key_file.write(key)
            logger.info(f"Key generated and saved to '{key_path}'.")
        else:
            with open(key_path, 'rb') as key_file:
                key = key_file.read()
            logger.info(f"Key loaded from '{key_path}'.")
        return key

    @staticmethod
    def encrypt_yaml(input_yaml_path, output_path='config/config.ox', key_path='config/ox_key.key'):
        """Encrypt YAML file."""
        key = SecureFileManager.load_or_create_key(key_path)
        fernet = Fernet(key)

        if not os.path.exists(input_yaml_path):
            raise FileNotFoundError(f"File '{input_yaml_path}' not found.")

        with open(input_yaml_path, 'r') as file:
            data = file.read()
        encrypted_data = fernet.encrypt(data.encode())

        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'wb') as encrypted_file:
            encrypted_file.write(encrypted_data)
        logger.info(f"YAML encrypted to '{output_path}'.")

    @staticmethod
    def decrypt_ox(ox_file_path, key_path='config/ox_key.key'):
        """Decrypt .ox file."""
        key = SecureFileManager.load_or_create_key(key_path)
        fernet = Fernet(key)

        if not os.path.exists(ox_file_path):
            raise FileNotFoundError(f"File '{ox_file_path}' not found.")

        with open(ox_file_path, 'rb') as file:
            encrypted_data = file.read()
        decrypted_data = fernet.decrypt(encrypted_data).decode()
        return yaml.safe_load(decrypted_data)

class Quoma:
    def __init__(self):
        self.security_hash = None
        self.execution_log = []

    def compute_hash(self, file_path):
        """Compute secure hash for a file."""
        try:
            with open(file_path, 'rb') as file:
                file_data = file.read()
                self.security_hash = hashlib.sha256(file_data).hexdigest()
                logger.info(f"Hash for '{file_path}': {self.security_hash}")
        except Exception as e:
            logger.error(f"Error computing hash: {e}")

    def extract_metadata(self, root_dir):
        """Extract functions and comments from Python files."""
        code_files = [os.path.join(root, f) for root, _, files in os.walk(root_dir) for f in files if f.endswith('.py')]
        dataset = []

        for file in code_files:
            with open(file, "r", encoding="utf-8") as f:
                try:
                    tree = ast.parse(f.read())
                    for node in ast.walk(tree):
                        if isinstance(node, ast.FunctionDef):
                            dataset.append({
                                "file": file,
                                "name": node.name,
                                "start": node.lineno,
                                "end": getattr(node, "end_lineno", node.lineno)
                            })
                except Exception:
                    continue
        return pd.DataFrame(dataset)

    def add_quantum_features(self, dataset):
        """Add quantum features to the dataset."""
        dataset["quantum_features"] = dataset["name"].apply(map_code_to_quantum_features)
        return dataset

# Main Script
if __name__ == "__main__":
    if len(sys.argv) < 2:
        logger.error("Usage: python script.py <file|directory>")
        sys.exit(1)

    input_path = sys.argv[1]
    quoma = Quoma()

    if os.path.isfile(input_path):
        quoma.compute_hash(input_path)
    elif os.path.isdir(input_path):
        dataset = quoma.extract_metadata(input_path)
        dataset = quoma.add_quantum_features(dataset)
        dataset.to_csv("metadata_with_quantum_features.csv", index=False)
        logger.info("Metadata with quantum features saved to 'metadata_with_quantum_features.csv'.")