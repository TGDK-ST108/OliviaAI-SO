from cryptography.fernet import Fernet

# Encrypt the URI first (do this outside of your application and store the key securely)
encryption_key = b'https://OliviaAI.vault.azure.net/'  # Securely generate and store this key elsewhere
encrypted_uri = b"gAAAAAB...="  # Result from encrypting your URI

# Decrypt within your application
fernet = Fernet(encryption_key)
key_vault_uri = fernet.decrypt(encrypted_uri).decode()
