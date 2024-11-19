import logging

class DynamicPrivacyGuard:
    def __init__(self):
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    def enforce_privacy_policy(self, data):
        """Simulate enforcing a privacy policy on given data."""
        # Example: Redact sensitive information
        if 'sensitive' in data:
            logging.info("Sensitive data detected. Redacting...")
            data['sensitive'] = 'REDACTED'
        logging.info("Privacy policy enforced.")
        return data

# Example usage
if __name__ == "__main__":
    privacy_guard = DynamicPrivacyGuard()
    sample_data = {'name': 'Alice', 'sensitive': 'Secret Info'}
    protected_data = privacy_guard.enforce_privacy_policy(sample_data)
    print("Protected data:", protected_data)
