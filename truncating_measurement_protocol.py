import logging

class TruncatingMeasurementProtocol:
    def __init__(self, truncation_threshold):
        self.truncation_threshold = truncation_threshold
        self.measurements = []
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    def record_measurement(self, value):
        """Record a measurement value."""
        self.measurements.append(value)
        logging.info(f"Recorded measurement: {value}")

    def truncate_measurements(self):
        """Truncate measurements based on the defined threshold."""
        if not self.measurements:
            logging.warning("No measurements to truncate.")
            return []

        truncated_measurements = [m for m in self.measurements if m < self.truncation_threshold]
        logging.info(f"Truncated measurements: {truncated_measurements}")
        return truncated_measurements

    def clear_measurements(self):
        """Clear all recorded measurements."""
        self.measurements.clear()
        logging.info("Cleared all measurements.")

# Example usage:
if __name__ == "__main__":
    # Create an instance of the protocol with a truncation threshold of 10
    protocol = TruncatingMeasurementProtocol(truncation_threshold=10)

    # Record some measurements
    protocol.record_measurement(5)
    protocol.record_measurement(15)
    protocol.record_measurement(8)
    protocol.record_measurement(12)

    # Truncate measurements
    truncated = protocol.truncate_measurements()
    print("Truncated Measurements:", truncated)

    # Clear measurements
    protocol.clear_measurements()
