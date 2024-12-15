class OverwatchMonitor:
    def __init__(self):
        self.activity_logs = []

    def start_monitoring(self, system_name):
        print(f"Starting live monitoring for {system_name}...")
        # Placeholder for actual monitoring logic
        return {"status": "monitoring", "system": system_name}

    def log_activity(self, system_name, activity):
        log_entry = {"system": system_name, "activity": activity, "timestamp": self.get_timestamp()}
        self.activity_logs.append(log_entry)
        print(f"Logged activity for {system_name}: {activity}")

    @staticmethod
    def get_timestamp():
        import datetime
        return datetime.datetime.now().isoformat()

    def report_anomalies(self, system_name):
        print(f"Scanning {system_name} logs for anomalies...")
        # Placeholder for anomaly detection logic
        detected_anomalies = [log for log in self.activity_logs if "anomaly" in log["activity"]]
        if detected_anomalies:
            print(f"Anomalies detected in {system_name}: {detected_anomalies}")
            return detected_anomalies
        print(f"No anomalies detected in {system_name}.")
        return None