import os
import yaml
import logging
from cryptography.fernet import Fernet
from azure.quantum import Workspace
from azure.quantum.qiskit import AzureQuantumProvider
from azure.identity import DefaultAzureCredential

def create_config_file(config_path, key_path):
    """Allows the user to input Azure Quantum workspace details and generates an encrypted config file."""
    try:
        # Collect input details
        print("Please provide the Azure Quantum Workspace details.")
        subscription_id = input("Subscription ID: ")
        resource_group = input("Resource Group: ")
        workspace_name = input("Workspace Name: ")
        location = input("Workspace Location (e.g., eastus): ")

        config = {
            "quantum_workspace": {
                "subscription_id": subscription_id,
                "resource_group": resource_group,
                "workspace_name": workspace_name,
                "location": location
            },
            "additional_services": {}
        }

        # Generate an encryption key
        key = Fernet.generate_key()
        with open(key_path, "wb") as key_file:
            key_file.write(key)

        # Encrypt the configuration
        fernet = Fernet(key)
        encrypted_data = fernet.encrypt(yaml.dump(config).encode("utf-8"))

        with open(config_path, "wb") as config_file:
            config_file.write(encrypted_data)

        print(f"Configuration file created and encrypted at {config_path}.")
    except Exception as e:
        print(f"Error creating configuration file: {e}")

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AzureCredentialManager:
    def __init__(self, config_path: str, key_path: str):
        self.config = None
        self.key_path = key_path
        self.config_path = config_path
        self.services = {}

    def decrypt_config(self):
        """Decrypts and loads the configuration file."""
        try:
            with open(self.key_path, "rb") as key_file:
                key = key_file.read()
            fernet = Fernet(key)

            with open(self.config_path, "rb") as encrypted_file:
                encrypted_data = encrypted_file.read()

            decrypted_data = fernet.decrypt(encrypted_data).decode("utf-8")
            self.config = yaml.safe_load(decrypted_data)
            logger.info("Configuration successfully decrypted and loaded.")
        except Exception as e:
            logger.error(f"Failed to decrypt or load configuration: {e}")
            raise

    def setup_workspace(self):
        """Sets up the Azure Quantum workspace based on the decrypted configuration."""
        try:
            quantum_workspace = self.config.get("quantum_workspace", {})
            if not quantum_workspace:
                logger.warning("Quantum workspace configuration missing. Disabling Quantum services.")
                self.services["quantum"] = None
                return

            subscription_id = quantum_workspace.get("subscription_id")
            resource_group = quantum_workspace.get("resource_group")
            workspace_name = quantum_workspace.get("workspace_name")
            location = quantum_workspace.get("location")

            if not (subscription_id and resource_group and workspace_name and location):
                logger.warning("Incomplete Quantum workspace configuration. Disabling Quantum services.")
                self.services["quantum"] = None
                return

            # Initialize workspace
            credential = DefaultAzureCredential()
            workspace = Workspace(
                subscription_id=subscription_id,
                resource_group=resource_group,
                name=workspace_name,
                location=location,
                credential=credential
            )
            self.services["quantum"] = {
                "workspace": workspace,
                "provider": AzureQuantumProvider(workspace=workspace)
            }
            logger.info("Azure Quantum workspace initialized successfully.")
        except Exception as e:
            logger.error(f"Failed to set up Azure Quantum workspace: {e}")
            self.services["quantum"] = None

    def setup_additional_services(self):
        """Sets up other services based on the configuration."""
        additional_services = self.config.get("additional_services", {})
        for service_name, service_config in additional_services.items():
            try:
                if service_config.get("enabled"):
                    logger.info(f"Initializing {service_name}...")
                    # Example: Add real initialization here
                    self.services[service_name] = {
                        "details": service_config,
                        "status": "initialized"
                    }
                else:
                    logger.info(f"{service_name} is disabled in the configuration.")
                    self.services[service_name] = None
            except Exception as e:
                logger.error(f"Failed to initialize {service_name}: {e}")
                self.services[service_name] = None

    def is_service_enabled(self, service_name: str) -> bool:
        """Checks if a given service is enabled and initialized."""
        return self.services.get(service_name) is not None

    def get_service(self, service_name: str):
        """Retrieves the initialized service details."""
        return self.services.get(service_name)

    def run(self):
        """Main execution to load configuration and initialize services."""
        self.decrypt_config()
        self.setup_workspace()
        self.setup_additional_services()

if __name__ == "__main__":
    config_path = "config/config.ox"
    key_path = "config/ox_key.key"

    # Check if configuration file exists; if not, create it
    if not os.path.exists(config_path):
        create_config_file(config_path, key_path)

    manager = AzureCredentialManager(config_path=config_path, key_path=key_path)

    try:
        manager.run()
        if manager.is_service_enabled("quantum"):
            quantum_service = manager.get_service("quantum")
            workspace = quantum_service["workspace"]
            provider = quantum_service["provider"]

            # List available Quantum backends
            targets = workspace.get_targets()
            print("Available Quantum targets:")
            for target in targets:
                print(f"- {target.id}")

    except Exception as e:
        logger.error(f"Error during execution: {e}")
