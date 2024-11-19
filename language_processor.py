import logging
from dual_fragmented_successionary_predicate_sequencer import DualFragmentedSuccessionaryPredicateSequencer

class LanguageProcessor:
    """Processes language input for sentiment analysis, entity recognition, and code handling."""

    def __init__(self):
        # Initialize the DualFragmentedSuccessionaryPredicateSequencer
        self.sequencer = DualFragmentedSuccessionaryPredicateSequencer()
        self.last_text = None
        self.last_sentiment_score = None
        self.last_entities = None

    def analyze_text(self, text: str, lang: str = None):
        """Analyzes text for sentiment and entities and applies etiquette using the Sequencer."""
        logging.info("Starting language analysis and etiquette processing.")
        self.last_text = text
        self.last_sentiment_score, self.last_entities = self.sequencer.apply_etiquette(text, lang)
        
        return self.last_sentiment_score, self.last_entities

    def preprocess_text(self, text: str, lang: str = None) -> str:
        """Preprocess text using the Sequencer's quantum-enhanced methods."""
        logging.info("Preprocessing text.")
        preprocessed_text = self.sequencer.preprocess(text, lang)
        return preprocessed_text

    def handle_code(self, code: str, language: str) -> str:
        """Processes code snippets with the Sequencer."""
        logging.info(f"Processing code in {language}.")
        return self.sequencer.handle_code_particles(code, language)

    def process_system_file(self, file_path: str) -> str:
        """Processes system files of various types using the Sequencer."""
        logging.info(f"Processing system file: {file_path}.")
        return self.sequencer.process_system_file(file_path)

    def get_language_summary(self):
        """Returns a summary of the latest text analysis."""
        return (
            f"Text Analyzed: {self.last_text}\n"
            f"Sentiment Score: {self.last_sentiment_score}\n"
            f"Entities: {', '.join(self.last_entities) if self.last_entities else 'None'}"
        )
