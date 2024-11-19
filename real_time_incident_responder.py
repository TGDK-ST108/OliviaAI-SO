import logging

class RealTimeIncidentResponder:
    def __init__(self):
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    def respond_to_incident(self, incident):
        """Simulate responding to a security incident."""
        logging.info(f"Responding to incident: {incident}")
        # Here, we could include logic for handling the incident
        self.contain_incident(incident)

    def contain_incident(self, incident):
        """Contain the incident to prevent further damage."""
        logging.info(f"Incident contained: {incident}")

# Example usage
if __name__ == "__main__":
    responder = RealTimeIncidentResponder()
    responder.respond_to_incident("Unauthorized access detected.")
