class MultiFactorAuthenticationSystem:
    def __init__(self):
        self.user_manager = UserManager()
        self.otp_manager = OTPManager()
        self.sessions = {}  # Session storage

    def register_user(self, username, password, email):
        self.user_manager.add_user(username, password)
        otp_secret = self.otp_manager.generate_otp_secret()
        self.user_manager.users[username]["otp_secret"] = otp_secret
        self.user_manager.users[username]["email"] = email

    def login(self, username, password):
        # Step 1: Verify password
        if not self.user_manager.authenticate_password(username, password):
            return False, "Invalid password"

        # Step 2: Send OTP for second-factor authentication
        user = self.user_manager.users[username]
        otp_code = self.otp_manager.generate_otp(user["otp_secret"])
        self.otp_manager._send_email_otp(user["email"], otp_code)

        # Mark as password authenticated, pending OTP verification
        self.sessions[username] = {"password_authenticated": True, "otp_verified": False}
        return True, "OTP sent"

    def verify_otp(self, username, otp_code):
        user = self.user_manager.users.get(username)
        if not user:
            return False, "User not found"

        # Verify OTP
        if self.otp_manager.verify_otp(user["otp_secret"], otp_code):
            self.sessions[username]["otp_verified"] = True
            return True, "Login successful"
        return False, "Invalid OTP"
