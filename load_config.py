# Import necessary modules
import logging
import yaml
import os

# Define the load_config function
def load_config(config_path='config.yaml'):
    """
    Load configuration from a YAML file.

    Parameters:
    - config_path (str): The path to the configuration file. Defaults to 'config.yaml'.

    Returns:
    - dict: The loaded configuration as a dictionary.
    """
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        full_config_path = os.path.join(script_dir, config_path)

        with open(full_config_path, 'r') as config_file:
            config = yaml.safe_load(config_file)
        return config
    except FileNotFoundError as e:
        raise Exception(f"Configuration file not found at: {full_config_path}") from e
    except yaml.YAMLError as e:
        raise Exception(f"Error loading YAML configuration: {e}") from e
    except Exception as e:
        raise Exception(f"Unexpected error while loading configuration: {e}") from e


def get_config_value(config, keys, default_value=None):
    """
    Retrieve a nested configuration value safely.

    Parameters:
    - config (dict): The configuration dictionary.
    - keys (list): A list of keys representing the path to the desired value.
    - default_value: The default value to return if the key path is not found.

    Returns:
    - The value from the configuration dictionary, or default_value if not found.
    """
    value = config
    try:
        for key in keys:
            value = value[key]
    except KeyError:
        return default_value
    return value


# Main script
if __name__ == "__main__":
    # Set up logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    try:
        # Load the configuration
        config = load_config()

        # Use the get_config_value function to retrieve values
        key_vault_uri = get_config_value(config, ["key_vault", "uri"])
        network_ranges = get_config_value(config, ["network_ranges"])
        resource_id = get_config_value(config, ["quantum_workspace", "resource_id"])

        # Use the loaded config in SteelOx initialization
        steelox = SteelOx(
            config=config,
            key_vault_uri=key_vault_uri,
            network_ranges=network_ranges,
            resource_id=resource_id
        )
        logger.info("SteelOx initialized successfully.")

        # Run service threads and workflows
        steelox.run_service_threads()
        logger.info("Service threads started.")
        steelox.run_infinite_workflow()

    except KeyError as e:
        logger.error(f"Missing configuration key: {e}")
        sys.exit(1)
    except Exception as e:
        logger.exception(f"An error occurred during SteelOx initialization: {e}")
        sys.exit(1)


# Load the key for decryption
    def load_encryption_key(key_path='ox_key.key'):
        try:
            with open(key_path, 'rb') as key_file:
                key = key_file.read()
            logger.info("Encryption key loaded successfully.")
            return key
        except FileNotFoundError:
            logger.error(f"Encryption key file '{key_path}' not found.")
            raise

# Load configuration from an .ox file
    def load_from_ox_file(ox_file_path='config.ox', key=None):
        try:
            if key is None:
                # Load key from file if not provided
                key = load_encryption_key()

            # Initialize Fernet with the key
            fernet = Fernet(key)

            # Read the encrypted configuration from the .ox file
            with open(ox_file_path, 'rb') as ox_file:
                encrypted_config = ox_file.read()

            # Decrypt the configuration string
            decrypted_config_str = fernet.decrypt(encrypted_config).decode()

            # Deserialize JSON string to dictionary
            config = json.loads(decrypted_config_str)
            logger.info(f"Configuration successfully loaded from '{ox_file_path}'.")
            return config
        except Exception as e:
            logger.error(f"Failed to load configuration from '{ox_file_path}': {e}")
            raise

if __name__ == "__main__":
    # Load configuration from .ox file
    config = load_from_ox_file()

    # Debug print configuration to verify it loads correctly
    logger.debug(json.dumps(config, indent=2))