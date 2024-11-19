import logging

logging.basicConfig(filename="firewall.log", level=logging.INFO)

class LoggingSystem:
    def log_event(self, event_type, details):
        logging.info(f"{event_type}: {details}")

    def alert(self, message):
        print("ALERT:", message)  # Can replace with an email alert system

# Example usage
logger = LoggingSystem()
logger.log_event("Suspicious Traffic", "Blocked packet from IP 192.168.1.10")
logger.alert("Multiple anomalies detected")
