class CrossSystemIntrusionDetection:
    def __init__(self, olivia_ai):
        self.olivia_ai = olivia_ai

    def monitor_systems(self, connected_systems):
        # Monitor multiple systems for suspicious activity
        intrusion_logs = []
        for system in connected_systems:
            logs = self.olivia_ai.analyze("system_intrusion_logs", system)
            intrusion_logs.append(logs)
        return intrusion_logs

    def detect_coordinated_attacks(self, intrusion_logs):
        # Analyze logs for patterns indicating coordinated attacks
        attack_patterns = self.olivia_ai.analyze("coordinated_attack_patterns", intrusion_logs)
        return attack_patterns