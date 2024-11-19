import re
import yaml
import os

class AzureQuantumConfigValidator:
    def __init__(self, config):
        self.config = config.get("quantum_workspace", {})

    def validate(self):
        """
        Validates Azure Quantum configuration settings.

        Raises:
            ValueError: If any configuration is missing or incorrectly formatted.
        """
        self._validate_connection_string()
        self._validate_resource_id()
        self._validate_workspace_id()
        self._validate_subscription_id()
        self._validate_location()
        print("Azure Quantum configuration is valid.")

    def _validate_connection_string(self):
        """Validate the format of the connection string."""
        connection_string = self.config.get("connection_string")
        if not connection_string:
            raise ValueError("Connection string is missing in the configuration.")
        
        # Simple pattern to match key-value pairs in the connection string
        pattern = (
            r"SubscriptionId=[a-fA-F0-9-]+;"
            r"ResourceGroupName=[\w-]+;"
            r"WorkspaceName=[\w-]+;"
            r"ApiKey=[\w-]+;"
            r"QuantumEndpoint=https://[a-z]+\.quantum\.azure\.com/;"
        )
        if not re.match(pattern, connection_string):
            raise ValueError("Connection string format is invalid.")

    def _validate_resource_id(self):
        """Validate the Azure Quantum resource ID format."""
        resource_id = self.config.get("resource_id")
        if not resource_id:
            raise ValueError("Resource ID is missing in the configuration.")
        
        pattern = (
            r"^/subscriptions/[a-fA-F0-9-]+/resourceGroups/[a-zA-Z0-9-_]+"
            r"/providers/Microsoft\.Quantum/Workspaces/[a-zA-Z0-9-_]+$"
        )
        if not re.match(pattern, resource_id):
            raise ValueError("Resource ID format is invalid. Expected format: "
                             "/subscriptions/{subscription_id}/resourceGroups/{resource_group}/providers/"
                             "Microsoft.Quantum/Workspaces/{workspace_name}")

    def _validate_workspace_id(self):
        """Validate that workspace_id matches resource_id if both are provided."""
        workspace_id = self.config.get("workspace_id")
        if workspace_id and workspace_id != self.config.get("resource_id"):
            raise ValueError("Workspace ID must match Resource ID.")

    def _validate_subscription_id(self):
        """Validate the subscription ID format."""
        subscription_id = self.config.get("subscription_id")
        if not subscription_id:
            raise ValueError("Subscription ID is missing in the configuration.")

        if not re.match(r"^[a-fA-F0-9-]{36}$", subscription_id):
            raise ValueError("Subscription ID format is invalid.")

    def _validate_location(self):
        """Validate the Azure location format (workspace_location)."""
        location = self.config.get("workspace_location")
        if not location:
            raise ValueError("Workspace location is missing in the configuration.")

        # Check for alphanumeric Azure region naming pattern, e.g., japaneast, eastus, westeurope
        if not re.match(r"^[a-z]+$", location):
            raise ValueError("Workspace location format is invalid.")

def load_config_from_yaml(file_path="config.yaml"):
    """Load configuration from a YAML file."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The configuration file {file_path} does not exist.")
    
    with open(file_path, 'r') as file:
        config = yaml.safe_load(file)
    return config

# Usage example
try:
    config = load_config_from_yaml("config.yaml")
    validator = AzureQuantumConfigValidator(config)
    validator.validate()
except (FileNotFoundError, ValueError) as e:
    print(f"Validation error: {e}")
