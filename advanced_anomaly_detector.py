import numpy as np
import logging

class AdvancedAnomalyDetector:
    def __init__(self, threshold=2.0):
        self.threshold = threshold
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    def detect_anomalies(self, data):
        """Detect anomalies in the dataset based on standard deviation."""
        mean = np.mean(data)
        std_dev = np.std(data)
        anomalies = [x for x in data if abs(x - mean) > self.threshold * std_dev]
        logging.info(f"Detected anomalies: {anomalies}")
        return anomalies

# Example usage
if __name__ == "__main__":
    detector = AdvancedAnomalyDetector(threshold=1.5)
    sample_data = np.array([1, 2, 3, 4, 100, 5, 6])
    anomalies = detector.detect_anomalies(sample_data)
    print("Anomalies detected:", anomalies)
