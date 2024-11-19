from textblob import TextBlob
import logging

class SentimentAnalyzer:
    def __init__(self):
        logging.info("Sentiment Analyzer initialized.")

    def analyze(self, text):
        """Analyzes the sentiment of the given text using TextBlob."""
        try:
            analysis = TextBlob(text)
            polarity = analysis.sentiment.polarity
            subjectivity = analysis.sentiment.subjectivity

            # Determine sentiment based on polarity
            if polarity > 0:
                sentiment = 'Positive'
            elif polarity < 0:
                sentiment = 'Negative'
            else:
                sentiment = 'Neutral'

            # Log the analysis
            logging.info(f"Text analyzed: {text}")
            logging.info(f"Polarity: {polarity}, Subjectivity: {subjectivity}, Sentiment: {sentiment}")

            # Return results as a dictionary
            return {
                'text': text,
                'polarity': polarity,
                'subjectivity': subjectivity,
                'sentiment': sentiment
            }
        except Exception as e:
            logging.error(f"Error during sentiment analysis: {e}")
            return None
