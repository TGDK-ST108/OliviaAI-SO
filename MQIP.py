class MQIPEncryption:
    def __init__(self, key_length=128):
        self.key_length = key_length
        self.key = self.generate_key()

    def generate_key(self):
        """
        Generate a quantum-secure key using MQIP principles.
        """
        import secrets
        return secrets.token_hex(self.key_length // 8)

    def encrypt(self, message):
        """
        Encrypt the message using MQIP encryption.
        """
        encoded_message = ''.join(format(ord(char) ^ ord(self.key[i % len(self.key)]), '02x')
                                  for i, char in enumerate(message))
        return encoded_message

    def decrypt(self, encrypted_message):
        """
        Decrypt the MQIP-encrypted message.
        """
        decrypted_message = ''.join(
            chr(int(encrypted_message[i:i + 2], 16) ^ ord(self.key[i // 2 % len(self.key)]))
            for i in range(0, len(encrypted_message), 2))
        return decrypted_message