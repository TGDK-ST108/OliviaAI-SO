import os
import json
import logging
import yaml
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from quantum_sdk_toolkit import QuantumFeatureMapper, QuantumOptimizer

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EnhancedQuantumFeatureMapper(QuantumFeatureMapper):
    def __init__(self, config: dict, num_qubits: int):
        """
        Enhanced Quantum Feature Mapper, extending QuantumFeatureMapper.

        Parameters:
        - config (dict): Configuration dictionary containing backend and provider details.
        - num_qubits (int): Number of qubits for quantum operations.
        """
        # Extract provider name from the config
        provider_name = config.get("quantum_workspace", {}).get("provider", "IonQ")
        
        # Initialize the parent class
        super().__init__(provider=provider_name, num_qubits=num_qubits)
        
        self.config = config
        self.backend = None

    def select_backend(self):
        """Select and configure the backend from the configuration."""
        try:
            backend_name = self.config["quantum_workspace"].get("backend_name")
            if not backend_name:
                raise ValueError("Backend name not specified in the configuration.")
            
            # Ensure self.backend is properly initialized as an object
            available_backends = self.get_available_backends()
            matching_backends = [b for b in available_backends if b.name == backend_name]
            
            if not matching_backends:
                raise ValueError(f"Backend '{backend_name}' not found among available backends.")
            
            self.backend = matching_backends[0]
            logger.info(f"Selected backend: {self.backend.name}")
        except Exception as e:
            logger.error(f"Failed to select backend: {e}")
            raise



# Load YAML configuration
config_path = "config/config.yaml"
num_qubits = 4

try:
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Configuration file not found at {config_path}")

    with open(config_path, "r") as yaml_file:
        config = yaml.safe_load(yaml_file)
    logger.info("Configuration successfully loaded.")
except Exception as e:
    logger.error(f"Failed to load configuration: {e}")
    exit()

# Initialize Quantum Mapper
try:
    quantum_mapper = EnhancedQuantumFeatureMapper(config, num_qubits)
    quantum_mapper.select_backend()
except Exception as e:
    logger.error(f"Quantum mapper initialization failed: {e}")
    exit()

# Load dataset
try:
    dataset = pd.read_csv("code_dataset.csv")
    if "name" not in dataset.columns or "label" not in dataset.columns:
        raise KeyError("Dataset missing required columns: 'name', 'label'")
    logger.info("Dataset loaded successfully.")
except (FileNotFoundError, KeyError) as e:
    logger.error(f"Dataset error: {e}")
    exit()

# Add Quantum Features
def generate_quantum_features(name):
    try:
        return quantum_mapper.run_quantum_circuit(
            quantum_mapper.map_features([len(name), sum(ord(c) for c in name)])
        )
    except Exception as e:
        logger.error(f"Error generating quantum features for {name}: {e}")
        return None

dataset["quantum_features"] = dataset["name"].apply(generate_quantum_features)

# Advanced feature processing
def compressional_factoring(features):
    return np.log1p(np.abs(features))

def distributive_shielding(features):
    return np.tanh(features)

def compressional_bifactoring(features):
    return compressional_factoring(features) * distributive_shielding(features)

try:
    dataset["factored_features"] = dataset["quantum_features"].apply(compressional_factoring)
    dataset["shielded_features"] = dataset["quantum_features"].apply(distributive_shielding)
    dataset["bifactored_features"] = dataset["quantum_features"].apply(compressional_bifactoring)
except Exception as e:
    logger.error(f"Feature processing failed: {e}")
    exit()

# Extract features and labels
try:
    X = np.array(dataset["quantum_features"].tolist())
    y = dataset["label"].tolist()
except KeyError:
    logger.error("Required columns not found in the dataset.")
    exit()

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train Random Forest Classifier
clf = RandomForestClassifier(n_estimators=100, random_state=42)
try:
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    logger.info(f"Random Forest Accuracy: {accuracy:.2f}")
except ValueError as e:
    logger.error(f"Model training failed: {e}")
    exit()

# Save enhanced dataset
dataset.to_csv("enhanced_code_dataset.csv", index=False)
logger.info("Enhanced dataset saved to 'enhanced_code_dataset.csv'.")
