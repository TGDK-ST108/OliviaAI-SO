import logging
from datetime import datetime

class RoundTableManager:
    def __init__(self, roundtable_api, olivia):
        """Initialize RoundTableManager with the roundtable API and Olivia instance."""
        self.roundtable_api = roundtable_api
        self.olivia = olivia
        self.participant_logs = {}  # Store logs per participant and topic
        self.topic_logs = {}        # Store logs per topic for organized discussion
        self.prediction_cache = {}  # Cache predictions for quick access

    def add_participant(self, participant_name):
        """Add a new participant to the roundtable if not already present."""
        if participant_name not in self.participant_logs:
            self.participant_logs[participant_name] = []
            logging.info(f"Added new participant: {participant_name}")
        else:
            logging.info(f"Participant {participant_name} already exists.")

    def log_discussion(self, message, participant_name="Unknown", topic="General"):
        """Log a message in the discussion with participant and topic information."""
        timestamp = datetime.now().isoformat()
        log_entry = f"[{timestamp}] {participant_name}: {message}"
        logging.info(log_entry)

        # Log by participant
        if participant_name in self.participant_logs:
            self.participant_logs[participant_name].append(log_entry)
        else:
            self.participant_logs[participant_name] = [log_entry]

        # Log by topic
        if topic in self.topic_logs:
            self.topic_logs[topic].append(log_entry)
        else:
            self.topic_logs[topic] = [log_entry]

    def facilitate_discussion(self, topic, participant_name="Moderator"):
        """Facilitate a discussion on a specified topic."""
        response = self.olivia.communicate(f"Discussing topic: {topic}")
        self.log_discussion(response, participant_name, topic)
        return response

    def summarize_discussions(self, topic=None):
        """
        Summarize all discussions held in the roundtable, or for a specific topic.
        """
        if topic and topic in self.topic_logs:
            summary = " | ".join(self.topic_logs[topic])
            print(f"RoundTable Summary for '{topic}': {summary}")
        else:
            summary = " | ".join(sum(self.topic_logs.values(), []))  # Summarize all topics
            print("Overall RoundTable Summary:", summary)
        return summary

    def export_discussions(self, filename="roundtable_log.txt"):
        """Export all discussions to a text file."""
        with open(filename, "w") as f:
            for topic, logs in self.topic_logs.items():
                f.write(f"Topic: {topic}\n")
                f.write("\n".join(logs) + "\n\n")
        logging.info(f"Exported discussions to {filename}")

    def analyze_discussion_sentiment(self, topic="General"):
        """
        Analyze the sentiment of a discussion topic, if roundtable API or Olivia supports it.
        """
        if topic in self.topic_logs:
            discussion_text = " ".join(self.topic_logs[topic])
            sentiment = self.roundtable_api.analyze_sentiment(discussion_text)
            print(f"Sentiment for topic '{topic}': {sentiment}")
            return sentiment
        else:
            logging.warning(f"No discussions found for topic '{topic}'")
            return None

    def generate_quantum_prediction(self, topic="General"):
        """
        Generate a quantum prediction for the specified topic, using quantum algorithms.
        Caches results for quick retrieval if the prediction was recently requested.
        """
        if topic in self.prediction_cache:
            logging.info(f"Retrieving cached prediction for topic '{topic}'")
            return self.prediction_cache[topic]

        if topic not in self.topic_logs:
            logging.warning(f"No discussions found for topic '{topic}'")
            return None

        # Prepare the data for prediction
        discussion_text = " ".join(self.topic_logs[topic])

        # Use the roundtable API or Olivia to generate quantum predictions
        try:
            prediction = self.roundtable_api.quantum_predict(discussion_text)
            self.prediction_cache[topic] = prediction
            logging.info(f"Quantum prediction generated for topic '{topic}': {prediction}")
            return prediction
        except AttributeError:
            logging.error("Quantum prediction capability not found in roundtable API.")
            return "Quantum prediction capability is unavailable."
