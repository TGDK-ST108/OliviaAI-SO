import bcrypt

class UserManager:
    def __init__(self):
        self.users = {}  # Simple in-memory user store, replace with a database for production

    def add_user(self, username, password):
        password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        self.users[username] = {"password_hash": password_hash, "otp_secret": None}

    def authenticate_password(self, username, password):
        user = self.users.get(username)
        if user and bcrypt.checkpw(password.encode(), user["password_hash"]):
            return True
        return False
