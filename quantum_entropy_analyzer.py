import os
import numpy as np
import yaml
from azure.quantum.qiskit import AzureQuantumProvider
from azure.quantum import Workspace
from qiskit import QuantumCircuit, transpile
from scipy.stats import entropy as shannon_entropy
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import logging

# Initialize logger
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class QuantumEntropyAnalyzer:
    def __init__(self, config_path='config.yaml'):
        with open("config.yaml", 'r') as config_file:
            config = yaml.safe_load(config_file)

            # Access the quantum workspace configuration
            azure_config = config.get('quantum_workspace', {})

            

            connection_string = azure_config.get('connection_string')
            resource_id = azure_config.get('resource_id')
            workspace_location = azure_config.get('workspace_location')
            subscription_id = azure_config.get('subscription_id')
            resource_group = azure_config.get('resource_group')
            workspace_name = azure_config.get('workspace_name')
            backend_name = azure_config.get('backend', 'ionq.simulator')
            # Initialize Workspace
            if connection_string:
                workspace = Workspace.from_connection_string(connection_string)
                logger.info("Initialized Workspace using connection string.")
            elif resource_id and workspace_location:
                workspace = Workspace(resource_id=resource_id, location=workspace_location)
                logger.info("Initialized Workspace using RESOURCE_ID and WORKSPACE_LOCATION.")
            elif workspace_name and subscription_id and resource_group and workspace_location:
                workspace = Workspace(
                    subscription_id=subscription_id,
                    resource_group=resource_group,
                    name=workspace_name,
                    location=workspace_location
                )
                logger.info("Initialized Workspace using individual parameters.")
            else:
                raise ValueError("Incomplete Azure Quantum workspace configuration in YAML.")

            # Initialize Azure Quantum provider
            self.provider = AzureQuantumProvider(workspace=workspace)
            self.backend = self.provider.get_backend(backend_name)
            logger.info(f"Selected backend: {self.backend.name}")

    def calculate_classical_entropy(self, data):
        """Calculate classical Shannon entropy with granularity based on data length."""
        num_qubits = len(data)
        probabilities, _ = np.histogram(data, bins=2 ** num_qubits, density=True)
        return shannon_entropy(probabilities, base=2)

    def create_quantum_circuit(self, data):
        """Map data to a quantum circuit with a dynamic number of qubits."""
        num_qubits = len(data)
        qc = QuantumCircuit(num_qubits, num_qubits)
        for i, val in enumerate(data):
            angle = np.pi * val
            qc.rx(angle, i)
            qc.ry(angle / 2, i)
            if i < num_qubits - 1:
                qc.cx(i, i + 1)
        qc.measure(range(num_qubits), range(num_qubits))
        return qc

    def calculate_quantum_entropy(self, qc):
        """Calculate entropy based on measurement probabilities."""
        transpiled_circuit = transpile(qc, self.backend)
        job = self.backend.run(transpiled_circuit, shots=1024)
        result = job.result()
        counts = result.get_counts()
        total_counts = sum(counts.values())
        probabilities = np.array(list(counts.values())) / total_counts
        return shannon_entropy(probabilities, base=2)

    def repeated_entropy_measurement(self, data, runs=30):
        """Run multiple entropy measurements to ensure stability."""
        num_qubits = len(data)
        results = []
        for _ in range(runs):
            perturbed_data = data + np.random.normal(0, 0.01, num_qubits)
            qc = self.create_quantum_circuit(perturbed_data)
            results.append(self.calculate_quantum_entropy(qc))
        return np.mean(results), np.std(results)

    def parallel_entropy_analysis(self, data_segments):
        """Parallel entropy analysis on data segments for efficiency."""
        with ThreadPoolExecutor() as executor:
            futures = [
                executor.submit(self.analyze_data_entropy, data) for data in data_segments
            ]
            results = [future.result() for future in futures]
        return results

    def analyze_data_entropy(self, data):
        """Full entropy analysis with enhanced quantum and classical measures."""
        classical_entropy = self.calculate_classical_entropy(data)
        quantum_entropy, quantum_entropy_std = self.repeated_entropy_measurement(data)

        return {
            "classical_entropy": classical_entropy,
            "quantum_entropy_mean": quantum_entropy,
            "quantum_entropy_std_dev": quantum_entropy_std
        }

if __name__ == "__main__":
    try:
        analyzer = QuantumEntropyAnalyzer(config_path='config.yaml')
        data_segments = [np.random.rand(6) for _ in range(30)]
        parallel_results = analyzer.parallel_entropy_analysis(data_segments)
        print("Parallel Entropy Analysis Example:", parallel_results[0])
    
    except Exception as e:
        logger.exception("An error occurred during entropy analysis")
