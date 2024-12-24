class GlobalThreatIntelligence:
    def __init__(self, olivia_ai):
        self.olivia_ai = olivia_ai

    def aggregate_threat_data(self, external_sources):
        # Collect threat intelligence from global sources
        aggregated_data = self.olivia_ai.aggregate("threat_intelligence", external_sources)
        return aggregated_data

    def share_threat_updates(self, local_data):
        # Share threat insights with trusted networks
        shared_status = self.olivia_ai.execute("share_threat_updates", local_data)
        return shared_status

    def receive_updates(self):
        # Retrieve the latest global threat intelligence
        updates = self.olivia_ai.retrieve("global_threat_updates", {})
        return updates