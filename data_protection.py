# data_protection.py
import logging
from cryptography.fernet import Fernet

class DataProtection:
    def __init__(self, encryption_key=None):
        if encryption_key is None:
            encryption_key = Fernet.generate_key()
            logging.info("Generated a new encryption key.")
        self.fernet = Fernet(encryption_key)
        logging.info("DataProtection initialized with encryption capabilities.")
        
    def encrypt_data(self, data: bytes) -> bytes:
        """Encrypt data using Fernet symmetric encryption."""
        logging.info("Encrypting data.")
        encrypted_data = self.fernet.encrypt(data)
        logging.debug(f"Encrypted data: {encrypted_data}")
        return encrypted_data
    
    def decrypt_data(self, encrypted_data: bytes) -> bytes:
        """Decrypt data that was encrypted using Fernet symmetric encryption."""
        logging.info("Decrypting data.")
        decrypted_data = self.fernet.decrypt(encrypted_data)
        logging.debug(f"Decrypted data: {decrypted_data}")
        return decrypted_data
    
    def log_access(self, user: str, access_type: str, data_reference: str):
        """Log access events, useful for auditing and compliance."""
        logging.info(f"Data accessed by {user} - Access type: {access_type} - Data reference: {data_reference}")
    
    def enforce_access_policy(self, user: str, required_role: str) -> bool:
        """Enforce an access policy based on user roles."""
        # Here you'd integrate with a user role database or system.
        # For demonstration, assuming all users have 'basic' role.
        user_role = 'basic'  # Placeholder for actual role lookup
        if user_role != required_role:
            logging.warning(f"Access denied for {user}. Required role: {required_role}, User role: {user_role}")
            return False
        logging.info(f"Access granted for {user}. Required role: {required_role}")
        return True

# Example usage of DataProtection
if __name__ == "__main__":
    # Initialize data protection with a specific key (for demo purposes)
    encryption_key = Fernet.generate_key()
    data_protection = DataProtection(encryption_key=encryption_key)
    
    # Encrypt and decrypt data
    original_data = b"Sensitive Information"
    encrypted_data = data_protection.encrypt_data(original_data)
    decrypted_data = data_protection.decrypt_data(encrypted_data)
    
    # Log access and enforce policy
    data_protection.log_access(user="Alice", access_type="read", data_reference="Document123")
    access_granted = data_protection.enforce_access_policy(user="Alice", required_role="admin")
    
    print("Original Data:", original_data)
    print("Encrypted Data:", encrypted_data)
    print("Decrypted Data:", decrypted_data)
    print("Access Granted:", access_granted)
