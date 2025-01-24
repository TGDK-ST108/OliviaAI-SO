import os
import json
import datetime
import hashlib
import secrets
import smtplib
from email.mime.text import MIMEText
from flask import Flask, request, jsonify
import jwt
from cryptography.fernet import Fernet
import quantum_sdk_toolkit as qstk  # OliviaAI’s Quantum AI Toolkit
from blockchain_sdk import QuantumNexusBlockchain  # Secure Blockchain for API Key Monitoring

# Secure API Key Monitoring Deployment
app = Flask(__name__)
SECRET_KEY = "TGDK_SECURE_API_NOTIFICATIONS"
MAX_FAILED_ATTEMPTS = 5  # Set threshold for blocking repeated unauthorized access
ADMIN_EMAIL = "admin@tgdk-security.com"  # Change this to your actual admin email

class TGDKAPIKeySecurity:
    def __init__(self):
        self.log_file = "tgdk_api_security_log.json"
        self.secure_storage = "secure_api_security.enc"
        self.blocked_ips = "blocked_ips.json"
        self.encryption_key = self.load_or_generate_key()
        self.blockchain = QuantumNexusBlockchain()
        self.failed_attempts = self.load_failed_attempts()

    def load_or_generate_key(self):
        """Loads or generates an encryption key for API security storage."""
        key_file = "quantum_api_security_encryption.key"
        if os.path.exists(key_file):
            with open(key_file, "rb") as f:
                return f.read()
        key = Fernet.generate_key()
        with open(key_file, "wb") as f:
            f.write(key)
        return key

    def encrypt_data(self, data):
        """Encrypts security logs before storage using Quantum Encryption."""
        cipher = Fernet(self.encryption_key)
        return cipher.encrypt(json.dumps(data).encode())

    def decrypt_data(self, encrypted_data):
        """Decrypts stored API security logs securely."""
        cipher = Fernet(self.encryption_key)
        return json.loads(cipher.decrypt(encrypted_data).decode())

    def log_api_usage(self, api_key, status, ip_address):
        """Logs API key usage and detects unauthorized access attempts."""
        log_entry = {
            "timestamp": datetime.datetime.now().isoformat(),
            "api_key": api_key,
            "status": status,
            "ip_address": ip_address
        }
        logs = []
        if os.path.exists(self.log_file):
            with open(self.log_file, "r") as f:
                logs = json.load(f)
        logs.append(log_entry)
        with open(self.log_file, "w") as f:
            json.dump(logs, f, indent=4)

        # Store event in Quantum Nexus Blockchain for security tracking
        self.blockchain.store_event(log_entry)

        # Detect Unauthorized API Key Usage
        if status == "unauthorized":
            self.record_failed_attempt(ip_address)
            self.trigger_security_response(api_key, ip_address)

        print(f"[SECURITY LOG] API Key: {api_key} | Status: {status} | IP: {ip_address}")

    def record_failed_attempt(self, ip_address):
        """Tracks failed API key attempts and blocks repeated offenders."""
        if ip_address not in self.failed_attempts:
            self.failed_attempts[ip_address] = 0
        self.failed_attempts[ip_address] += 1

        if self.failed_attempts[ip_address] >= MAX_FAILED_ATTEMPTS:
            self.block_ip(ip_address)

        # Save failed attempts
        with open(self.blocked_ips, "w") as f:
            json.dump(self.failed_attempts, f)

    def block_ip(self, ip_address):
        """Blocks an IP address after repeated unauthorized access attempts."""
        print(f"[SECURITY ALERT] Blocking IP: {ip_address} due to repeated unauthorized attempts.")
        self.failed_attempts[ip_address] = "BLOCKED"

        # Store blocked IP in Quantum Nexus Blockchain for security tracking
        self.blockchain.store_event({"event": "IP_BLOCKED", "ip_address": ip_address})

        # Send Security Notification
        self.send_security_notification(ip_address)

    def send_security_notification(self, ip_address):
        """Sends a security alert notification to the admin."""
        subject = "⚠️ TGDK AI Security Alert: IP Blocked"
        message = f"""
        ALERT: Unauthorized access attempts detected.

        - Blocked IP Address: {ip_address}
        - Time: {datetime.datetime.now().isoformat()}
        - Action: IP has been blocked after repeated failed API key attempts.

        Review the security logs in the Quantum Nexus Blockchain for further analysis.
        """

        self.send_email_notification(subject, message)
        print(f"[SECURITY NOTIFICATION] Sent alert to admin for blocked IP: {ip_address}")

    def send_email_notification(self, subject, message):
        """Sends an email notification for security events."""
        try:
            msg = MIMEText(message)
            msg["Subject"] = subject
            msg["From"] = "security-alerts@tgdk.com"
            msg["To"] = ADMIN_EMAIL

            with smtplib.SMTP("smtp.mailtrap.io", 587) as server:  # Change SMTP settings as needed
                server.login("your_username", "your_password")  # Use real SMTP credentials
                server.sendmail("security-alerts@tgdk.com", ADMIN_EMAIL, msg.as_string())

            print("[EMAIL SENT] Security alert notification sent successfully.")

        except Exception as e:
            print(f"[ERROR] Failed to send email notification: {e}")

    def load_failed_attempts(self):
        """Loads stored failed attempts from JSON file."""
        if os.path.exists(self.blocked_ips):
            with open(self.blocked_ips, "r") as f:
                return json.load(f)
        return {}

# Secure API Key Monitoring API Endpoints
@app.route('/monitor_api_key', methods=['POST'])
def monitor_api_key():
    """API Endpoint to monitor API key usage and log access attempts."""
    data = request.json
    api_key = data.get("api_key")
    ip_address = request.remote_addr

    security_monitor = TGDKAPIKeySecurity()

    # Check if IP is already blocked
    if ip_address in security_monitor.failed_attempts and security_monitor.failed_attempts[ip_address] == "BLOCKED":
        return jsonify({"error": "Your IP has been blocked due to repeated unauthorized attempts."}), 403

    status = "authorized" if verify_api_key(api_key) else "unauthorized"
    security_monitor.log_api_usage(api_key, status, ip_address)

    if status == "unauthorized":
        return jsonify({"error": "Unauthorized API Key Access Detected"}), 403

    return jsonify({"message": "API Key Access Logged Securely"}), 200

def verify_api_key(api_key):
    """Verifies if an API key is valid."""
    valid_api_keys = retrieve_stored_api_keys()
    return any(key["api_key"] == api_key for key in valid_api_keys)

def retrieve_stored_api_keys():
    """Retrieves stored API keys securely."""
    if os.path.exists("secure_api_keys.enc"):
        with open("secure_api_keys.enc", "rb") as f:
            encrypted_data = f.read()
        return TGDKAPIKeySecurity().decrypt_data(encrypted_data)
    return []

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5016)