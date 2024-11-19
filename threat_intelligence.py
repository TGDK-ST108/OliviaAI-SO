import logging
import requests

class ThreatIntelligence:
    def __init__(self, feed_url=None):
        self.feed_url = feed_url
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    
    def fetch_threats(self):
        """Fetches the latest threats from an external feed."""
        if not self.feed_url:
            logging.warning("No feed URL provided for threat intelligence.")
            return []
        
        response = requests.get(self.feed_url)
        if response.status_code == 200:
            logging.info("Successfully fetched threat data.")
            return response.json()  # Assuming the feed returns JSON
        else:
            logging.error("Failed to fetch threat data.")
            return []

    def gather_threat_data(self):
        """Simulate gathering threat intelligence data."""
        # Example data; in practice, this could be dynamically fetched from feeds
        threat_data = [
            {"threat": "Malware", "severity": "High", "source_ip": "192.168.1.10"},
            {"threat": "Phishing", "severity": "Medium", "source_ip": "192.168.1.15"},
            {"threat": "Ransomware", "severity": "Critical", "source_ip": "192.168.1.20"},
            {"threat": "Suspicious Activity", "severity": "Low", "source_ip": "192.168.1.25"},
        ]
        logging.info("Gathered threat data.")
        return threat_data

    def analyze_threats(self, threat_data):
        """Analyze gathered threat data and log findings."""
        for threat in threat_data:
            logging.info(f"Threat: {threat['threat']}, Severity: {threat['severity']}, Source IP: {threat['source_ip']}")

    def singularity_fragmentalizer(self, threat_data):
        """
        Detect fraudulent or suspicious signals in threat data, log them, and return the source IPs of suspicious activities.
        """
        fraudulent_ips = []
        
        for threat in threat_data:
            # Identifying fraudulent or suspicious signals based on threat severity
            if threat['severity'] in ["High", "Critical"]:
                logging.warning(f"Suspicious activity detected! Threat: {threat['threat']} from IP: {threat['source_ip']}")
                fraudulent_ips.append(threat['source_ip'])
        
        if not fraudulent_ips:
            logging.info("No fraudulent signals detected in the current threat data.")
        
        return fraudulent_ips

# Example usage
if __name__ == "__main__":
    ti = ThreatIntelligence(feed_url="https://example.com/threat-feed")
    data = ti.gather_threat_data()
    ti.analyze_threats(data)
    
    # Use the Singularity Fragmentalizer to detect and log suspicious activity
    fraudulent_ips = ti.singularity_fragmentalizer(data)
    logging.info(f"List of detected suspicious IPs: {fraudulent_ips}")
