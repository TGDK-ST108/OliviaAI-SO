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
from steelox_enhanced import SteelOxEnhanced

config_path = os.path.join(os.path.dirname(__file__), 'config.yaml')

class RoundTableAPI:
    def __init__(self, config_file='config.yaml'):
        # Initialize attributes
        self.api_keys = {}
        self.steelox_api = None
        self.data_store = {}

        # Load configuration
        self.load_config(config_file)

        # Ensure base_url is set
        if not hasattr(self, 'base_url'):
            raise AttributeError("Base URL not set. Please check your configuration.")

        print(f"API initialized with base URL: {self.base_url}")
        print(f"Endpoints: {self.endpoints}")

    def load_config(self, config_file):
        """Load API configurations from a YAML file."""
        try:
            with open(config_file, 'r') as file:
                config = yaml.safe_load(file)
            print("Config loaded:", config)  # Debug statement

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

            self.secret_key = config.get('secret_key')
            if not self.secret_key:
                raise ValueError("Secret key not found in configuration.")

        except FileNotFoundError:
            raise FileNotFoundError(f"Configuration file '{config_file}' not found.")
        except yaml.YAMLError as e:
            raise ValueError(f"Error parsing YAML configuration: {e}")
        except Exception as e:
            raise Exception(f"An error occurred while loading configuration: {e}")

    def generate_softset_key(self, user_id, permissions=None, expiration=3600):
        """Generate and store a softset API key matching the 64-character hexadecimal format."""
        key_bytes = hmac.new(
            self.secret_key.encode('utf-8'),
            uuid.uuid4().bytes,
            hashlib.sha256
        ).digest()
        key = key_bytes.hex()
        self.api_keys[key] = {
            'user_id': user_id,
            'permissions': permissions or {'send': True, 'fetch': True, 'update': True, 'delete': True},
            'expiration': time.time() + expiration
        }
        return key

    def validate_softset_key(self, key, endpoint):
        """Validate the softset API key and check permissions."""
        if not isinstance(key, str) or len(key) != 64:
            return False
        key_data = self.api_keys.get(key)
        if not key_data:
            return False
        if time.time() > key_data['expiration']:
            del self.api_keys[key]
            return False
        return key_data['permissions'].get(endpoint, False)

    def get_fernet_key(self):
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
            return fernet_key
        except binascii.Error as e:
            raise ValueError(f"Invalid secret key format: {e}")

    def send_data(self, data, identifier='default_id', api_key=None):
        """Send data to the API endpoint specified in the configuration."""
        if not self.validate_softset_key(api_key, 'send'):
            return {'error': 'Invalid or expired API key'}

        url = f"{self.base_url}/{self.endpoints['send']}"
        payload = {'id': identifier, 'data': data}
        headers = self.headers.copy()
        headers['Authorization'] = f'Bearer {api_key}'

        try:
            response = requests.post(url, json=payload, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
            return {'error': str(e)}

    # Similarly update fetch_data, update_data, delete_data methods...

    def revoke_api_key(self, key):
        """Revoke an existing API key."""
        if key in self.api_keys:
            del self.api_keys[key]
            return True
        return False

    def rotate_secret_key(self):
        """Rotate the secret key and invalidate all existing API keys."""
        new_secret_key = hashlib.sha256(uuid.uuid4().bytes).hexdigest()
        self.secret_key = new_secret_key
        self.api_keys.clear()
        # Update the secret key in the configuration file or secure storage
        print(f"New secret key: {self.secret_key}")

# Example usage
if __name__ == "__main__":
    api = RoundTableAPI(config_file=config_path)

    # Get the Fernet key
    fernet_key = api.get_fernet_key()

    # Initialize SteelOxEnhanced with the Fernet key
    steel_ox = SteelOxEnhanced(fernet_key)

    # Generate a test API key
    test_key = api.generate_softset_key(user_id="OliviaAI")
    print(f"Generated test API key: {test_key}")
    print(f"API key length: {len(test_key)}")
