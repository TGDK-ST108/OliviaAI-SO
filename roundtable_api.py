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
from azure.keyvault.secrets import SecretClient
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
        self.api_keys = self.get_api_keys()

    def load_config(self, config_file):
        """Load API configurations from a YAML file."""
        try:
            with open(config_file, 'r') as file:
                config = yaml.safe_load(file)

            # General settings
            self.config = config

            # Load base_url and endpoints
            api_config = config.get('api_config')
            if not api_config:
                raise ValueError("api_config section is missing in the configuration file.")

            self.base_url = api_config.get('base_url', 'https://default-base-url.com')
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
            key_bytes = binascii.unhexlify(hex_key)
            fernet_key = base64.urlsafe_b64encode(key_bytes)
            if len(base64.urlsafe_b64decode(fernet_key)) != 32:
                raise ValueError("Invalid secret key length. Fernet key must be 32 bytes.")
            return fernet_key.decode('utf-8')
        except binascii.Error as e:
            raise ValueError(f"Invalid secret key format: {e}")

    def get_api_keys(self) -> List[str]:
        """
        Retrieves a list of valid API keys from Azure Key Vault.
        """
        try:
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
        """
        app = Flask(__name__)
        app.config['SECRET_KEY'] = self.secret_key

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

        @app.route('/add_blocked_port', methods=['POST'])
        @self.require_api_key_decorator
        def add_port():
            data = request.get_json()
            port = data.get('port')
            if not port or not (0 < port < 65536):
                return jsonify({"error": "Valid port number is required."}), 400
            self.threat_hunting.add_blocked_port(port)
            return jsonify({"message": f"Port {port} has been blocked."}), 200

        @app.route('/remove_blocked_port', methods=['POST'])
        @self.require_api_key_decorator
        def remove_port():
            data = request.get_json()
            port = data.get('port')
            if not port or not (0 < port < 65536):
                return jsonify({"error": "Valid port number is required."}), 400
            self.threat_hunting.remove_blocked_port(port)
            return jsonify({"message": f"Port {port} has been unblocked."}), 200

        @app.route('/fetch_logs', methods=['GET'])
        @self.require_api_key_decorator
        def fetch_logs():
            logs = self.threat_hunting.get_logs()
            return jsonify({"logs": logs}), 200

        @app.route('/clear_logs', methods=['POST'])
        @self.require_api_key_decorator
        def clear_logs():
            self.threat_hunting.clear_logs()
            return jsonify({"message": "Logs have been cleared."}), 200

        @app.route('/block_ip_range', methods=['POST'])
        @self.require_api_key_decorator
        def block_ip_range():
            data = request.get_json()
            ip_range = data.get('range')
            if not ip_range:
                return jsonify({"error": "IP range is required."}), 400
            self.threat_hunting.add_blocked_ip_range(ip_range)
            return jsonify({"message": f"IP range {ip_range} has been blocked."}), 200

        @app.route('/unblock_ip_range', methods=['POST'])
        @self.require_api_key_decorator
        def unblock_ip_range():
            data = request.get_json()
            ip_range = data.get('range')
            if not ip_range:
                return jsonify({"error": "IP range is required."}), 400
            self.threat_hunting.remove_blocked_ip_range(ip_range)
            return jsonify({"message": f"IP range {ip_range} has been unblocked."}), 200

        @app.route('/get_blocked_entities', methods=['GET'])
        @self.require_api_key_decorator
        def get_blocked_entities():
            blocked_ips = list(self.threat_hunting.blocked_ips)
            blocked_ports = list(self.threat_hunting.blocked_ports)
            return jsonify({"blocked_ips": blocked_ips, "blocked_ports": blocked_ports}), 200

        @app.route('/add_whitelist', methods=['POST'])
        @self.require_api_key_decorator
        def add_whitelist():
            data = request.get_json()
            entity = data.get('entity')
            if not entity:
                return jsonify({"error": "Entity is required."}), 400
            self.threat_hunting.add_whitelist(entity)
            return jsonify({"message": f"Entity {entity} has been whitelisted."}), 200

        @app.route('/remove_whitelist', methods=['POST'])
        @self.require_api_key_decorator
        def remove_whitelist():
            data = request.get_json()
            entity = data.get('entity')
            if not entity:
                return jsonify({"error": "Entity is required."}), 400
            self.threat_hunting.remove_whitelist(entity)
            return jsonify({"message": f"Entity {entity} has been removed from the whitelist."}), 200

        @app.route('/check_status', methods=['GET'])
        @self.require_api_key_decorator
        def check_status():
            status = self.threat_hunting.get_status()
            return jsonify({"status": status}), 200

        @app.route('/restart_system', methods=['POST'])
        @self.require_api_key_decorator
        def restart_system():
            self.threat_hunting.restart()
            return jsonify({"message": "System has been restarted."}), 200

        @app.route('/shutdown_system', methods=['POST'])
        @self.require_api_key_decorator
        def shutdown_system():
            self.threat_hunting.shutdown()
            return jsonify({"message": "System has been shut down."}), 200

        return app

# Main function
def main():
    # Initialize the API instance
    api = RoundTableAPI()

    # Start the API server and other monitoring services
    app = api.create_flask_app()
    app.run(host='0.0.0.0', port=5000)

    # Keep the main thread alive to allow background threads to function
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Shutting down.")
        api.logger.info("System is shutting down.")

if __name__ == "__main__":
    main()