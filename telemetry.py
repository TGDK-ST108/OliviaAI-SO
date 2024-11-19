import logging
import time
import json

class TelemetryManager:
    def __init__(self, log_file='telemetry_log.json'):
        self.log_file = log_file
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        self.telemetry_data = []

    def log_event(self, event_type, event_data):
        """Log an event with its type and data."""
        timestamp = time.time()
        event_entry = {
            'timestamp': timestamp,
            'event_type': event_type,
            'event_data': event_data
        }
        self.telemetry_data.append(event_entry)
        logging.info(f"Logged event: {event_entry}")

    def save_logs(self):
        """Save telemetry data to a log file."""
        try:
            with open(self.log_file, 'a') as f:
                for entry in self.telemetry_data:
                    f.write(json.dumps(entry) + '\n')
            self.telemetry_data.clear()  # Clear the data after saving
            logging.info(f"Telemetry data saved to {self.log_file}")
        except Exception as e:
            logging.error(f"Failed to save telemetry logs: {e}")

    def report_performance(self, metric_name, value):
        """Log a performance metric."""
        self.log_event('performance', {'metric_name': metric_name, 'value': value})

    def report_error(self, error_message):
        """Log an error."""
        self.log_event('error', {'message': error_message})

    def report_usage(self, feature_name):
        """Log usage of a specific feature."""
        self.log_event('usage', {'feature_name': feature_name})

# Example usage:
if __name__ == "__main__":
    telemetry_manager = TelemetryManager()

    # Log some events
    telemetry_manager.report_usage('Feature A')
    telemetry_manager.report_performance('Load Time', 250)
    telemetry_manager.report_error('Failed to load resource')

    # Save the logs
    telemetry_manager.save_logs()
