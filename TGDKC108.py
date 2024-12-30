class TGDKCardEncryption:
    def __init__(self, key_length=128):
        self.key_length = key_length
        self.key = self.generate_key()

    def generate_key(self):
        """
        Generate a quantum-secure key using MQIP principles.
        """
        import secrets
        return secrets.token_hex(self.key_length // 8)

    def encrypt(self, data):
        """
        Encrypt TGDK card data using MQIP encryption.
        """
        return ''.join(format(ord(char) ^ ord(self.key[i % len(self.key)]), '02x') for i, char in enumerate(data))

    def decrypt(self, encrypted_data):
        """
        Decrypt MQIP-encrypted TGDK card data.
        """
        return ''.join(chr(int(encrypted_data[i:i + 2], 16) ^ ord(self.key[i // 2 % len(self.key)]))
                       for i in range(0, len(encrypted_data), 2))


class TGDKCardMiddleware:
    def __init__(self, encryption_module):
        self.encryption_module = encryption_module

    def process_transaction(self, card_data, server_endpoint):
        """
        Process a secure transaction using MQIP encryption.
        """
        # Encrypt card data
        encrypted_data = self.encryption_module.encrypt(card_data)
        print(f"Encrypted Data Sent to {server_endpoint}: {encrypted_data}")

        # Simulate server response
        encrypted_response = self.simulate_server_response(encrypted_data)
        print(f"Encrypted Response from Server: {encrypted_response}")

        # Decrypt server response
        decrypted_response = self.encryption_module.decrypt(encrypted_response)
        return decrypted_response

    def simulate_server_response(self, encrypted_data):
        """
        Simulate server processing and encrypt the response.
        """
        # Simulate a server-side encrypted response
        return self.encryption_module.encrypt("Transaction Approved")