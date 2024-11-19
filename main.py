import threading
import time
import yaml
from threat_hunting import ThreatHunting
from roundtable_api import RoundTableAPI

def get_config_path():
    if hasattr(sys, '_MEIPASS'):
        # Running in the PyInstaller bundled executable
        return os.path.join(sys._MEIPASS, 'config.yaml')
    else:
        # Running in the source environment
        return 'config.yaml'

def load_config(config_path):
    """Load configuration from a YAML file."""
    try:
        with open(config_path, 'r') as config_file:
            return yaml.safe_load(config_file)
    except Exception as e:
        print(f"Failed to load configuration file: {e}")
        return None

def main():
    # Load configuration
    config_path = "config.yaml"  # Path to the configuration file
    config = load_config(config_path)
    if not config:
        print("Configuration loading failed. Exiting.")
        return

    # Extract configurations
    key_vault_uri = config.get('key_vault', {}).get('uri')
    network_ranges = config.get('network_ranges')
    flask_host = config.get('flask', {}).get('host', '0.0.0.0')
    flask_port = config.get('flask', {}).get('port', 8080)
    monitoring_interval = config.get('monitoring_interval', 60)

    # Initialize ThreatHunting instance
    try:
        threat_hunting = ThreatHunting(
            key_vault_uri=key_vault_uri,
            network_ranges=network_ranges
        )
    except Exception as e:
        print(f"Failed to initialize ThreatHunting: {e}")
        return

    # Initialize RoundTableAPI with the same configuration
    try:
        roundtable_api = RoundTableAPI(config_file=config_path)
    except Exception as e:
        print(f"Failed to initialize RoundTableAPI: {e}")
        return

    # Start traffic monitoring in a separate thread to prevent blocking
    monitoring_thread = threading.Thread(target=threat_hunting.monitor_traffic, name="TrafficMonitorThread")
    monitoring_thread.start()
    print("Started traffic monitoring thread.")

    # Start RoundTableAPI's Flask app in a separate thread
    flask_thread = threading.Thread(
        target=lambda: roundtable_api.app.run(host=flask_host, port=flask_port),
        name="FlaskThread"
    )
    flask_thread.start()
    print("Started RoundTableAPI Flask thread.")

    # Perform network scans and log analysis in the main thread
    try:
        while True:
            # Periodically scan the network
            threat_hunting.scan_network()
            # Periodically analyze logs
            threat_hunting.analyze_logs()
            time.sleep(monitoring_interval)  # Wait for the specified interval
    except KeyboardInterrupt:
        print("Shutting down services.")
        threat_hunting.logger.info("Shutting down services.")
        # Perform any necessary cleanup here

if __name__ == "__main__":
    main()
