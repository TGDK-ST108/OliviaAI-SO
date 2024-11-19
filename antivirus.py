import logging
import os

class Antivirus:
    def __init__(self):
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    def scan_file(self, file_path):
        """Simulate scanning a file for viruses."""
        if os.path.exists(file_path):
            logging.info(f"Scanning file: {file_path}")
            # Simulate scan logic
            infected = self.simulate_virus_check(file_path)
            if infected:
                logging.warning(f"Virus detected in file: {file_path}")
            else:
                logging.info(f"No virus detected in file: {file_path}")
        else:
            logging.error(f"File not found: {file_path}")

    def simulate_virus_check(self, file_path):
        """Simulate a virus check (randomly returns True or False)."""
        # For real implementations, use virus definitions and actual scanning techniques.
        return False  # For demonstration, assume no virus is found.

# Example usage
if __name__ == "__main__":
    antivirus = Antivirus()
    antivirus.scan_file('example.txt')  # Change to a valid file path for actual testing
