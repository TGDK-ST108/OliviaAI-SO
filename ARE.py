class AIRejectionEngine:
    def __init__(self, olivia_ai):
        self.olivia_ai = olivia_ai

    def detect_external_ai(self, incoming_data):
        # Analyze incoming data for AI signatures
        detection = self.olivia_ai.analyze("ai_signature_detection", incoming_data)
        return detection

    def reject_unauthorized_ai(self, detection_results):
        # Reject external AI based on validation results
        if detection_results["status"] == "unauthorized":
            response = self.olivia_ai.execute("reject_connection", detection_results)
            return {"rejected": True, "response": response}
        return {"rejected": False, "response": "No action needed"}