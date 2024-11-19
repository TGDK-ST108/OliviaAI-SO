# IntrusionDetectionSystem.py
import re

class IntrusionDetectionSystem:
    def __init__(self):
        self.signatures = []  # List of known malicious patterns
        self.anomaly_model = IsolationForest(contamination=0.01)

    def load_signatures(self, signature_file):
        with open(signature_file, 'r') as f:
            for line in f:
                self.signatures.append(line.strip())

    def detect_intrusion(self, packet):
        # Signature-based detection
        payload = str(bytes(packet))
        for signature in self.signatures:
            if re.search(signature, payload):
                return True, "Signature Match"

        # Anomaly-based detection
        if packet.haslayer(IP):
            features = [packet[IP].src, packet[IP].dst, packet[IP].len]
            prediction = self.anomaly_model.predict([features])
            if prediction == -1:
                return True, "Anomaly Detected"
        return False, None
