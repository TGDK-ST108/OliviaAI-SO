# intrusion_detection_system.py

import logging
from sklearn.ensemble import IsolationForest
import numpy as np
import re

class IntrusionDetectionSystem:
    def __init__(self):
        """
        Initializes the Intrusion Detection System with an Isolation Forest model for anomaly detection.
        """
        self.anomaly_model = IsolationForest(n_estimators=100, contamination=0.01, random_state=42)
        self.logger = logging.getLogger(self.__class__.__name__)
        logging.basicConfig(level=logging.INFO)
        self.trained = False
        self.logger.info("Intrusion Detection System initialized with Isolation Forest model.")

    def train_model(self, training_data):
        """
        Trains the anomaly detection model using the provided training data.

        Parameters:
            training_data (list of lists): The feature vectors extracted from network packets.
        """
        try:
            if not training_data:
                self.logger.warning("No training data provided. Model training aborted.")
                return

            X = np.array(training_data)
            self.anomaly_model.fit(X)
            self.trained = True
            self.logger.info("Anomaly detection model trained successfully.")
        except Exception as e:
            self.logger.exception(f"Error training the anomaly detection model: {e}")

    def detect_intrusion(self, packet):
        """
        Detects intrusions based on the provided network packet.

        Parameters:
            packet (scapy.packet.Packet): The network packet to analyze.

        Returns:
            tuple: (intrusion_detected: bool, reason: str)
        """
        try:
            if not self.trained:
                self.logger.warning("Anomaly detection model is not trained. Cannot detect intrusions.")
                return False, "Model not trained"

            if IP not in packet:
                return False, "Non-IP packet"

            # Extract features from the packet
            features = self.extract_features(packet)
            if not features:
                return False, "Insufficient features"

            X = np.array(features).reshape(1, -1)
            prediction = self.anomaly_model.predict(X)

            # In IsolationForest, -1 indicates anomaly, 1 indicates normal
            if prediction[0] == -1:
                reason = self.analyze_anomaly(features)
                self.logger.info(f"Intrusion detected: {reason}")
                return True, reason

            return False, "No intrusion detected"

        except Exception as e:
            self.logger.exception(f"Error during intrusion detection: {e}")
            return False, f"Error: {e}"

    def extract_features(self, packet):
        """
        Extracts relevant features from a network packet for anomaly detection.

        Parameters:
            packet (scapy.packet.Packet): The network packet.

        Returns:
            list: A list of numerical features.
        """
        try:
            src_ip = packet[IP].src
            dst_ip = packet[IP].dst
            protocol = packet[IP].proto

            # Extract transport layer information
            if TCP in packet:
                sport = packet[TCP].sport
                dport = packet[TCP].dport
                flags = packet[TCP].flags
            elif UDP in packet:
                sport = packet[UDP].sport
                dport = packet[UDP].dport
                flags = 0  # UDP does not have flags
            else:
                sport = 0
                dport = 0
                flags = 0

            # Packet length
            length = len(packet)

            # Number of payload bytes
            payload = bytes(packet.payload)
            payload_length = len(payload)

            # Detect common patterns or suspicious payloads
            malicious_payload = self.detect_malicious_payload(payload)

            # Convert IP addresses to numeric representation
            src_ip_numeric = self.ip_to_numeric(src_ip)
            dst_ip_numeric = self.ip_to_numeric(dst_ip)

            # Combine all features
            features = [
                sum(src_ip_numeric),   # Simple aggregation of source IP octets
                sum(dst_ip_numeric),   # Simple aggregation of destination IP octets
                protocol,
                sport,
                dport,
                flags,
                length,
                payload_length,
                malicious_payload
            ]

            return features

        except Exception as e:
            self.logger.exception(f"Error extracting features from packet: {e}")
            return []

    def ip_to_numeric(self, ip_address):
        """
        Converts an IP address string to a numeric representation.

        Parameters:
            ip_address (str): The IP address (e.g., '192.168.1.1').

        Returns:
            list of int: Numeric representation of the IP address.
        """
        try:
            return [int(octet) for octet in ip_address.split('.')]
        except Exception as e:
            self.logger.exception(f"Error converting IP address to numeric: {e}")
            return [0, 0, 0, 0]

    def detect_malicious_payload(self, payload):
        """
        Detects malicious patterns in the payload.

        Parameters:
            payload (bytes): The payload of the network packet.

        Returns:
            int: 1 if malicious pattern is detected, else 0.
        """
        try:
            # Define suspicious patterns
            suspicious_patterns = [
                b'cmd=',            # Command injection
                b'<script>',        # XSS
                b'<?php',           # PHP injection
                b'UNION SELECT',    # SQL injection
                b'--',              # SQL comment
                b'base64_encode',   # Encoding commands
            ]

            for pattern in suspicious_patterns:
                if re.search(pattern, payload, re.IGNORECASE):
                    self.logger.debug(f"Malicious payload pattern detected: {pattern}")
                    return 1
            return 0
        except Exception as e:
            self.logger.exception(f"Error detecting malicious payload: {e}")
            return 0

    def analyze_anomaly(self, features):
        """
        Analyzes the features of an anomalous packet to determine the reason.

        Parameters:
            features (list): The feature vector of the packet.

        Returns:
            str: Reason for the anomaly.
        """
        try:
            malicious_payload = features[8]
            if malicious_payload:
                return "Malicious payload detected"

            packet_length = features[6]
            if packet_length > 1500:  # Example threshold
                return "Abnormally large packet size"

            # Add more detailed analysis as needed
            return "Anomaly detected based on model prediction"
        except Exception as e:
            self.logger.exception(f"Error analyzing anomaly: {e}")
            return "Anomaly detected"

