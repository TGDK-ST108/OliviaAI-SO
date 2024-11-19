class TransmissionReceptor:
    def __init__(self):
        """Initialize the TransmissionReceptor."""
        self.received_data = []
        self.transmission_log = []

    def receive_data(self, data):
        """
        Receive data and log the transmission.

        Args:
            data (any): The data to be received.
        """
        self.received_data.append(data)
        self.transmission_log.append(f"Received: {data}")
        print(f"Data received: {data}")

    def process_data(self):
        """
        Process the received data.

        Returns:
            list: The processed data.
        """
        processed_data = [self._process_single_data(d) for d in self.received_data]
        print("Data processed successfully.")
        return processed_data

    def _process_single_data(self, data):
        """
        Process a single piece of data.

        Args:
            data (any): The data to be processed.

        Returns:
            any: The processed data.
        """
        # Implement your data processing logic here
        processed = data * 0.5  # Example: Halving the value
        return processed

    def clear_received_data(self):
        """Clear all received data and reset the log."""
        self.received_data.clear()
        self.transmission_log.clear()
        print("Received data and transmission log cleared.")

    def display_log(self):
        """Display the transmission log."""
        print("Transmission Log:")
        for entry in self.transmission_log:
            print(entry)
