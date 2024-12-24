class GlobalHealthMonitoring:
    def __init__(self, olivia_ai):
        self.olivia_ai = olivia_ai

    def aggregate_health_data(self, human_data_stream, animal_data_stream):
        # Analyze global health trends
        combined_data = {"human_data": human_data_stream, "animal_data": animal_data_stream}
        trends = self.olivia_ai.analyze("global_health_trends", combined_data)
        outbreak_alerts = self.olivia_ai.predict("disease_outbreaks", trends)
        resource_recommendations = self.olivia_ai.feedback("resource_allocation", outbreak_alerts)
        return {"trends": trends, "outbreak_alerts": outbreak_alerts, "resource_recommendations": resource_recommendations}