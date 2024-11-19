import logging

class IntelligentThreatClassifier:
    def __init__(self):
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    def classify_threat(self, threat):
        """Classify a threat based on its characteristics."""
        threat_types = {
            "Malware": "High Risk",
            "Phishing": "Medium Risk",
            "Ransomware": "Critical Risk",
        }
        classification = threat_types.get(threat, "Unknown Threat")
        logging.info(f"Classified threat: {threat}, Classification: {classification}")
        return classification

# Example usage
if __name__ == "__main__":
    classifier = IntelligentThreatClassifier()
    threat = "Phishing"
    classification = classifier.classify_threat(threat)
    print("Threat classification:", classification)
