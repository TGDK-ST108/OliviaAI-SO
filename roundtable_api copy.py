# roundtable_api.py

import os
import requests
import json
import hashlib
import hmac
import uuid
import time
import yaml
import base64
import binascii
import logging
from typing import List, Dict, Any

from flask import Flask, request, jsonify
from functools import wraps

from azure.identity import DefaultAzureCredential, AzureCliCredential
from azure.kusto.data import KustoClient, KustoConnectionStringBuilder
from azure.keyvault.secrets import SecretClient
from azure.kusto.data.exceptions import KustoServiceError

from steelox_enhanced import SteelOxEnhanced
from threat_hunting import ThreatHunting  # Ensure this is the correct import path

config_path = os.path.join(os.path.dirname(__file__), 'config.yaml')

class RoundTableAPI:
    def __init__(self, config_file='config.yaml'):
        # Initialize attributes
        self.api_keys = {}
        self.steelox_api = None
        self.data_store = {}
        self.threat_hunting = None  # Will be initialized later

        # Load configuration
        self.load_config(config_file)

        # Ensure base_url is set
        if not hasattr(self, 'base_url'):
            raise AttributeError("Base URL not set. Please check your configuration.")

        print(f"API initialized with base URL: {self.base_url}")
        print(f"Endpoints: {self.endpoints}")

        # Initialize logging
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(name)s: %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

        # Initialize Key Vault client
        credential = AzureCliCredential()
        self.key_vault_client = SecretClient(vault_url=self.key_vault['uri'], credential=credential)

        # Initialize ThreatHunting
        self.threat_hunting = ThreatHunting(
            key_vault_uri=self.key_vault['uri'],
            network_ranges=self.network_ranges,
            roundtable_api=self  # Pass self to allow ThreatHunting to interact if needed
        )

        # Initialize SteelOxEnhanced
        self.steelox_api = SteelOxEnhanced(
            config=self.config,
            key_vault_uri=self.key_vault['uri'],
            network_ranges=self.network_ranges,
            resource_id=self.steelox['resource_id']
        )

        # Retrieve the Fernet key
        fernet_key = self.get_fernet_key()

        # Generate initial API keys
        self.generate_initial_api_keys()

        # Create Flask app
        self.app = self.create_flask_app()

    def generate_initial_api_keys(self):
        """
        Initialize API keys from configuration or generate new ones.
        """
        # Assuming you have a method to retrieve or generate API keys
        self.api_keys = self.get_api_keys()

    def load_config(self, config_file):
        """Load API configurations from a YAML file."""
        try:
            with open(config_file, 'r') as file:
                config = yaml.safe_load(file)
            print("Config loaded:", config)  # Debug statement

            # General settings
            self.config = config

            # Load base_url and endpoints
            api_config = config.get('api_config')
            if not api_config:
                raise ValueError("api_config section is missing in the configuration file.")

            print("API Config:", api_config)  # Debug statement

            self.base_url = api_config.get('base_url')
            if not self.base_url:
                print("base_url not found in api_config, using default.")
                self.base_url = 'https://olivia-tgdk.com'  # Default value

            print("Base URL set to:", self.base_url)  # Debug statement

            self.endpoints = api_config.get('endpoints', {
                'send': 'send_data',
                'fetch': 'fetch_data',
                'update': 'update_data',
                'delete': 'delete_data'
            })

            self.headers = api_config.get('headers', {})

            # Load key_vault settings
            self.key_vault = config.get('key_vault')
            if not self.key_vault:
                raise ValueError("key_vault section is missing in the configuration file.")

            # Load other configurations as needed
            self.network_ranges = config.get('network_ranges', [])
            self.whitelist = config.get('whitelist', [])
            self.blacklist = config.get('blacklist', [])
            self.cache = config.get('cache', {})
            self.rate_limiter = config.get('rate_limiter', {})
            self.load_balancer = config.get('load_balancer', {})
            self.steelox = config.get('steelox', {})

            # Add more configuration sections as necessary

            # Retrieve the secret_key from config
            self.secret_key = config.get('secret_key')
            if not self.secret_key:
                raise ValueError("Secret key not found in configuration.")

        except FileNotFoundError:
            raise FileNotFoundError(f"Configuration file '{config_file}' not found.")
        except yaml.YAMLError as e:
            raise ValueError(f"Error parsing YAML configuration: {e}")
        except Exception as e:
            raise Exception(f"An error occurred while loading configuration: {e}")

    def get_fernet_key(self) -> str:
        """Convert the hex secret key to a URL-safe base64-encoded key for Fernet."""
        hex_key = self.secret_key
        if not hex_key:
            raise ValueError("Secret key is missing.")
        try:
            # Convert hex string to bytes
            key_bytes = binascii.unhexlify(hex_key)
            # Base64 encode the key bytes
            fernet_key = base64.urlsafe_b64encode(key_bytes)
            # Fernet key must be 32 bytes after decoding
            if len(base64.urlsafe_b64decode(fernet_key)) != 32:
                raise ValueError("Invalid secret key length. Fernet key must be 32 bytes.")
            return fernet_key.decode('utf-8')  # Convert bytes to string for Fernet
        except binascii.Error as e:
            raise ValueError(f"Invalid secret key format: {e}")

    def get_api_keys(self) -> List[str]:
        """
        Retrieves a list of valid API keys from Azure Key Vault.

        Returns:
            List[str]: A list of API key strings.
        """
        try:
            # Assume API keys are stored with names like 'API-KEY-1', 'API-KEY-2', etc.
            api_keys = []
            for secret_properties in self.key_vault_client.list_properties_of_secrets():
                if secret_properties.name.startswith("API-KEY-"):
                    secret = self.key_vault_client.get_secret(secret_properties.name)
                    api_keys.append(secret.value)
            self.logger.info("Retrieved API keys from Key Vault.")
            return api_keys
        except Exception as e:
            self.logger.error(f"Failed to retrieve API keys: {e}")
            return []

    def validate_api_key(self, provided_key: str) -> bool:
        """
        Validates the provided API key against stored keys.

        Parameters:
            provided_key (str): The API key provided by the client.

        Returns:
            bool: True if valid, False otherwise.
        """
        hashed_provided_key = hashlib.sha256(provided_key.encode()).hexdigest()
        for key in self.api_keys:
            hashed_stored_key = hashlib.sha256(key.encode()).hexdigest()
            if hashed_provided_key == hashed_stored_key:
                self.logger.info("Valid API key provided.")
                return True
        self.logger.warning("Invalid API key provided.")
        return False

    def require_api_key_decorator(self, f):
        """
        Decorator to require API key for protected routes.

        Parameters:
            f: The route function.

        Returns:
            function: The decorated function.
        """
        @wraps(f)
        def decorated(*args, **kwargs):
            api_key = request.headers.get('X-API-KEY')
            if not api_key or not self.validate_api_key(api_key):
                self.logger.warning("Unauthorized access attempt detected.")
                return jsonify({"error": "Unauthorized"}), 401
            return f(*args, **kwargs)
        return decorated

    def create_flask_app(self) -> Flask:
        """
        Creates and configures the Flask application with secure endpoints.

        Returns:
            Flask: The configured Flask app.
        """
        app = Flask(__name__)
        app.config['SECRET_KEY'] = self.flask.get('secret_key', 'default_flask_secret_key')

        @app.route('/add_blocked_ip', methods=['POST'])
        @self.require_api_key_decorator
        def add_ip():
            data = request.get_json()
            ip = data.get('ip')
            if not ip:
                return jsonify({"error": "IP address is required."}), 400
            if not self.threat_hunting.is_valid_ip(ip):
                return jsonify({"error": "Invalid IP address format."}), 400
            self.threat_hunting.add_blocked_ip(ip)
            return jsonify({"message": f"IP {ip} has been blocked."}), 200

        @app.route('/remove_blocked_ip', methods=['POST'])
        @self.require_api_key_decorator
        def remove_ip():
            data = request.get_json()
            ip = data.get('ip')
            if not ip:
                return jsonify({"error": "IP address is required."}), 400
            self.threat_hunting.remove_blocked_ip(ip)
            return jsonify({"message": f"IP {ip} has been unblocked."}), 200

        @app.route('/add_blocked_port', methods=['POST'])
        @self.require_api_key_decorator
        def add_port():
            data = request.get_json()
            port = data.get('port')
            if port is None:
                return jsonify({"error": "Port number is required."}), 400
            try:
                port = int(port)
                if not (0 < port < 65536):
                    raise ValueError
            except ValueError:
                return jsonify({"error": "Invalid port number."}), 400
            self.threat_hunting.add_blocked_port(port)
            return jsonify({"message": f"Port {port} has been blocked."}), 200

        @app.route('/remove_blocked_port', methods=['POST'])
        @self.require_api_key_decorator
        def remove_port():
            data = request.get_json()
            port = data.get('port')
            if port is None:
                return jsonify({"error": "Port number is required."}), 400
            try:
                port = int(port)
                if not (0 < port < 65536):
                    raise ValueError
            except ValueError:
                return jsonify({"error": "Invalid port number."}), 400
            self.threat_hunting.remove_blocked_port(port)
            return jsonify({"message": f"Port {port} has been unblocked."}), 200

        # Add more API routes as needed

        return app

    def rotate_secret_key(self):
        """
        Rotate the secret key and invalidate all existing API keys.
        """
        new_secret_key = hashlib.sha256(uuid.uuid4().bytes).hexdigest()
        self.secret_key = new_secret_key
        self.api_keys.clear()
        # Update the secret key in the configuration file or secure storage
        self.logger.info(f"New secret key: {self.secret_key}")
        # You may need to update Key Vault with the new secret_key

    def run(self):
        """
        Runs the Flask app and starts the threat hunting monitoring in separate threads.
        """
        # Start Flask app in a separate thread
        flask_thread = threading.Thread(target=lambda: self.app.run(host='0.0.0.0', port=5000))
        flask_thread.daemon = True
        flask_thread.start()

        # Start ThreatHunting traffic monitoring
        self.threat_hunting.monitor_traffic()

# Example usage
if __name__ == "__main__":
    api = RoundTableAPI(config_file=config_path)

    # Start the API and threat hunting in separate threads
    api.run()

    # Keep the main thread alive
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Shutting down.")
