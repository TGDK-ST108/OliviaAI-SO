class QuantumCommunicator:
    def __init__(self, communication_framework):
        self.framework = communication_framework

    def send_message(self, message, target_location):
        """
        Send a quantum signal message to a target location.
        """
        encoded_message = self.framework.encode(message)
        response = self.framework.transmit(encoded_message, target_location)
        return response

# Example Usage
communication_framework = QuantumCommunicationFramework()
communicator = QuantumCommunicator(communication_framework)
response = communicator.send_message("Hello Mars", "Martian Outpost")
print("Communication Response:", response)