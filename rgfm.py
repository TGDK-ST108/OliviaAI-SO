from azure.quantum import Workspace
from azure.quantum.qiskit import AzureQuantumProvider
from qiskit import QuantumCircuit, transpile
from cryptography.fernet import Fernet
import json
import logging
from azure.quantum import Workspace

workspace = Workspace(
            resource_id = "/subscriptions/b282c457-292d-4181-96a4-169ac357585a/resourceGroups/OliviaAI_group/providers/Microsoft.Quantum/Workspaces/OliviaAIQuantum",
            location = "japaneast")

# Set up logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class TGDKQuantumFeatureMapper:
    def __init__(self, num_qubits: int):
        """
        Initialize the Azure Quantum Feature Mapper using a secure .ox config file.
        Args:
            config_file (str): Path to the encrypted .ox configuration file.
            key_path (str): Path to the encryption key file.
            num_qubits (int): Number of qubits for the quantum circuit.
        """
        self.num_qubits = num_qubits
        self.backend = None  # Backend will be selected dynamically

    
    def list_backends(self):
        """
        List all available backends from the Azure Quantum provider.
        """
        backends = self.provider.backends()
        print("Available Quantum Backends:")
        for i, backend in enumerate(backends):
            print(f"{i + 1}. {backend.name} - {backend.configuration().description}")
        return backends

    def select_backend(self, backend_name):
        available_backends = self.workspace.get_targets()
        for backend in available_backends:
            if backend.id == backend_name:
                self.backend = backend
                logging.info(f"Selected backend: {backend_name}")
                return
        raise ValueError(f"Backend {backend_name} not found. Available backends: {[b.id for b in available_backends]}")


    def map_features(self, features: list) -> QuantumCircuit:
        """
        Map classical features to quantum states using RX and RY rotations.
        Args:
            features (list): List of classical features.
        Returns:
            QuantumCircuit: A quantum circuit representing the feature mapping.
        """
        qc = QuantumCircuit(self.num_qubits, self.num_qubits)
        for i, feature in enumerate(features):
            if i < self.num_qubits:
                qc.rx(feature, i)
                qc.ry(feature, i)
        qc.measure(range(self.num_qubits), range(self.num_qubits))
        logger.debug(f"Quantum circuit created with features: {features}")
        return qc

    def run_quantum_circuit(self, qc: QuantumCircuit) -> dict:
        """
        Run quantum circuit on the selected Azure Quantum backend.
        Args:
            qc (QuantumCircuit): Quantum circuit to run.
        Returns:
            dict: Measurement results.
        """
        if self.backend is None:
            raise RuntimeError("Backend not selected. Please select a backend using 'select_backend' method.")

        try:
            transpiled_circuit = transpile(qc, self.backend)
            job = self.backend.run(transpiled_circuit)
            result = job.result()
            counts = result.get_counts()
            logger.info("Quantum job executed successfully.")
            return counts
        except Exception as e:
            logger.error(f"Failed to run quantum circuit: {e}")
            raise

# MAIN SCRIPT

if __name__ == "__main__":
    # Secure paths
    num_qubits = 2

    # Initialize TGDKQuantumFeatureMapper
    TGDK = TGDKQuantumFeatureMapper(num_qubits=num_qubits)

    # List available backends and select one
    available_backends = TGDK.list_backends()
    backend_choice = int(input("Select a backend (enter the number): "))
    selected_backend_name = available_backends[backend_choice - 1].name
    TGDK.select_backend(selected_backend_name)

    # Example feature vector
    feature_vector = [0.5, 1.2]

    # Create and run quantum circuit
    quantum_circuit = TGDK.map_features(feature_vector)
    quantum_results = TGDK.run_quantum_circuit(quantum_circuit)

    # Print results
    print("Quantum Results:", quantum_results)
