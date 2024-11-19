class EndpointEncryptionManager:
    def __init__(self, key_storage_path):
        self.key_manager = KeyManager(key_storage_path)
        self.encryption_manager = EncryptionManager(self.key_manager)
        self.user_auth = UserAuthentication()

    def register_user(self, username, password):
        self.user_auth.add_user(username, password)
        # Generate RSA keys protected by the user's password
        self.key_manager.generate_keys(username, password=password)
        print(f"[INFO] User '{username}' registered and keys generated.")

    def encrypt_file_for_user(self, username, password, file_path):
        if self.user_auth.authenticate(username, password):
            self.encryption_manager.encrypt_file(username, file_path)
        else:
            print("[ERROR] Authentication failed. Cannot encrypt file.")

    def decrypt_file_for_user(self, username, password, encrypted_file_path, output_path=None):
        if self.user_auth.authenticate(username, password):
            # Load the private key using the user's password
            self.key_manager.load_private_key(username, password=password)
            self.encryption_manager.decrypt_file(username, encrypted_file_path, output_path)
        else:
            print("[ERROR] Authentication failed. Cannot decrypt file.")
