# traffic_analyzer.py

import logging
from scapy.all import IP, TCP, UDP
from sklearn.ensemble import IsolationForest
import numpy as np
import re
import socket
import struct

class TrafficAnalyzer:
    def __init__(self):
        self.training_data = []
        self.model = None
        self.logger = logging.getLogger(self.__class__.__name__)
        logging.basicConfig(level=logging.INFO)

    def collect_training_data(self, packet):
        """
        Collect relevant features from each packet for training the anomaly detection model.
        """
        try:
            if IP not in packet:
                return  # Skip non-IP packets

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

            # Detect common patterns or suspicious payloads (simple example)
            malicious_payload = self.detect_malicious_payload(payload)

            # Convert IP addresses to numerical representations
            src_ip_numeric = self.ip_to_numeric(src_ip)
            dst_ip_numeric = self.ip_to_numeric(dst_ip)

            # Combine all features into a single list
            features = [
                src_ip_numeric,   # Source IP as numerical value
                dst_ip_numeric,   # Destination IP as numerical value
                protocol,
                sport,
                dport,
                flags,
                length,
                payload_length,
                malicious_payload
            ]

            self.training_data.append(features)
            self.logger.debug(f"Collected training data: {features}")

        except Exception as e:
            self.logger.exception(f"Error collecting training data: {e}")

    def train_model(self):
        """
        Train the anomaly detection model using the collected training data.
        """
        try:
            if not self.training_data:
                self.logger.warning("No training data collected. Cannot train the model.")
                return

            X = np.array(self.training_data)
            self.model = IsolationForest(n_estimators=100, contamination=0.01, random_state=42)
            self.model.fit(X)
            self.logger.info("Anomaly detection model trained successfully.")

        except Exception as e:
            self.logger.exception(f"Error training the model: {e}")

    def analyze_packet(self, packet):
        """
        Analyze a packet to determine if it's anomalous.
        Returns True if anomalous, else False.
        """
        try:
            if not self.model:
                self.logger.warning("Model not trained. Cannot analyze packets.")
                return False

            if IP not in packet:
                return False  # Non-IP packets are considered normal

            src_ip = packet[IP].src
            dst_ip = packet[IP].dst
            protocol = packet[IP].proto

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

            length = len(packet)
            payload = bytes(packet.payload)
            payload_length = len(payload)
            malicious_payload = self.detect_malicious_payload(payload)

            # Convert IP addresses to numerical representations
            src_ip_numeric = self.ip_to_numeric(src_ip)
            dst_ip_numeric = self.ip_to_numeric(dst_ip)

            # Combine all features into a single list
            features = [
                src_ip_numeric,   # Source IP as numerical value
                dst_ip_numeric,   # Destination IP as numerical value
                protocol,
                sport,
                dport,
                flags,
                length,
                payload_length,
                malicious_payload
            ]

            X = np.array(features).reshape(1, -1)
            prediction = self.model.predict(X)

            # In IsolationForest, -1 indicates anomaly, 1 indicates normal
            if prediction[0] == -1:
                self.logger.info(f"Anomalous packet detected from {src_ip}")
                return True
            return False

        except Exception as e:
            self.logger.exception(f"Error analyzing packet: {e}")
            return False

    def deep_inspect(self, packet):
        """
        Perform deep packet inspection to detect malicious payloads or patterns.
        Returns True if malicious content is found, else False.
        """
        try:
            if IP not in packet:
                return False  # Non-IP packets are considered clean

            # Example: Check for specific malicious payload signatures
            payload = bytes(packet.payload)
            if self.detect_malicious_payload(payload):
                self.logger.info(f"Malicious payload detected in packet from {packet[IP].src}")
                return True

            # Add more sophisticated inspections as needed
            return False

        except Exception as e:
            self.logger.exception(f"Error during deep packet inspection: {e}")
            return False

    def ip_to_numeric(self, ip_address):
        """
        Converts an IP address string to a single numerical value.
        This can be done by packing the IP into an integer.
        """
        try:
            packed_ip = socket.inet_aton(ip_address)
            numeric_ip = struct.unpack("!I", packed_ip)[0]
            return numeric_ip
        except Exception as e:
            self.logger.exception(f"Error converting IP address to numeric: {e}")
            return 0

    def detect_malicious_payload(self, payload):
        """
        Detects malicious patterns in the payload.
        Returns 1 if malicious pattern is detected, else 0.
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
