import secrets

SECRET_KEY = secrets.token_hex(32)
print(SECRET_KEY)
from auth_manager import QuantumLDAPAuthenticator
        self.auth_manager = QuantumLDAPAuthenticator()