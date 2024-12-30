class OliviaAISecurity:
    def __init__(self):
        self.api_base_url = "http://localhost:8000"  # Update with deployment URL
        self.logs = []

    def call_api(self, endpoint, data):
        """
        Call OliviaAI Cybersecurity API endpoints.
        """
        import requests
        try:
            response = requests.post(f"{self.api_base_url}{endpoint}", json=data)
            if response.status_code == 200:
                return response.json()
            else:
                self.log_error(f"API call failed: {response.status_code}, {response.text}")
                return None
        except Exception as e:
            self.log_error(f"Error calling API: {str(e)}")
            return None

    def log_error(self, error_message):
        self.logs.append(f"Error: {error_message}")
        print(f"Error: {error_message}")

# Example usage
olivia_ai_security = OliviaAISecurity()

# Analyze threats
threats = olivia_ai_security.call_api("/analyze-threats", {"data_stream": [10, 20, 30]})
print("Threat Analysis:", threats)

# Encrypt data
encryption = olivia_ai_security.call_api("/encrypt-data", {"plaintext": "Hello, World!", "key": 123})
print("Encrypted Data:", encryption)

# Decrypt data
decryption = olivia_ai_security.call_api("/decrypt-data", {"ciphertext": encryption['encrypted_text'], "key": 123})
print("Decrypted Data:", decryption)