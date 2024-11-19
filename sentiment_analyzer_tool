# sentiment_analysis_tool.py

from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from transformers import pipeline
from langdetect import detect
from googletrans import Translator
import logging
import numpy as np

class SentimentAnalyzer:
    def __init__(self, method='textblob', language='en'):
        """
        Initialize the SentimentAnalyzer with options for analysis method and default language.
        
        Parameters:
        - method: The sentiment analysis method to use ('textblob', 'vader', 'transformer').
        - language: The default language of the input text ('en' for English).
        """
        self.method = method
        self.language = language
        self.vader_analyzer = SentimentIntensityAnalyzer() if method == 'vader' else None
        self.transformer_analyzer = pipeline("sentiment-analysis") if method == 'transformer' else None
        self.translator = Translator()
        self.previous_sentiment = None  # For tracking derivative changes
        self.sequenced_results = []  # To hold sequenced sentiment results

    def analyze(self, text):
        """
        Perform sentiment analysis on the input text based on the selected method.
        Handles multiple languages by translating text when necessary.
        """
        logging.info("Performing sentiment analysis...")
        
        # Detect language and translate if needed
        detected_language = detect(text)
        if detected_language != self.language:
            text = self.translator.translate(text, src=detected_language, dest=self.language).text
            logging.info(f"Translated text to {self.language}: {text}")
        
        # Perform sentiment analysis based on the chosen method
        sentiment_result = None
        if self.method == 'textblob':
            sentiment_result = self._analyze_with_textblob(text)
        elif self.method == 'vader':
            sentiment_result = self._analyze_with_vader(text)
        elif self.method == 'transformer':
            sentiment_result = self._analyze_with_transformer(text)
        else:
            logging.error("Invalid sentiment analysis method selected.")
            return None

        # Calculate derivative sentiment (change over time)
        derivative_result = self._calculate_derivative(sentiment_result)
        
        # Perform causal effect analysis
        causal_effects = self._analyze_causal_effects(text)
        
        # Factorize sentiment result
        factorized_result = self._factorize_sentiment(sentiment_result)
        
        # Add to distribution sequencer and return result
        sequenced_result = self._sequence_distribution(sentiment_result)
        
        final_result = {
            "sentiment": sentiment_result,
            "derivative": derivative_result,
            "causal_effects": causal_effects,
            "factorized": factorized_result,
            "sequenced_results": sequenced_result
        }
        return final_result

    def _analyze_with_textblob(self, text):
        """Analyze sentiment using TextBlob."""
        blob = TextBlob(text)
        sentiment_score = blob.sentiment.polarity
        return {"polarity": sentiment_score, "sentiment": "positive" if sentiment_score > 0 else "negative" if sentiment_score < 0 else "neutral"}

    def _analyze_with_vader(self, text):
        """Analyze sentiment using VADER."""
        scores = self.vader_analyzer.polarity_scores(text)
        return {"polarity": scores['compound'], "positive": scores['pos'], "neutral": scores['neu'], "negative": scores['neg'], "sentiment": "positive" if scores['compound'] > 0 else "negative" if scores['compound'] < 0 else "neutral"}

    def _analyze_with_transformer(self, text):
        """Analyze sentiment using a Transformer-based model."""
        result = self.transformer_analyzer(text)[0]
        return {"label": result['label'], "score": result['score'], "sentiment": "positive" if "POSITIVE" in result['label'] else "negative"}

    def _calculate_derivative(self, current_sentiment):
        """Calculate the derivative sentiment to measure change over time."""
        if self.previous_sentiment is None:
            derivative = 0  # No previous sentiment to compare with
        else:
            derivative = current_sentiment['polarity'] - self.previous_sentiment['polarity']
        self.previous_sentiment = current_sentiment  # Update for next comparison
        return {"derivative": derivative}

    def _analyze_causal_effects(self, text):
        """Identify causal effects by detecting keywords that might impact sentiment."""
        causal_keywords = ['because', 'due to', 'since', 'therefore']
        causal_count = sum(text.lower().count(keyword) for keyword in causal_keywords)
        return {"causal_count": causal_count, "causal_effect_intensity": causal_count / len(text.split())}

    def _factorize_sentiment(self, sentiment):
        """Break down sentiment into more determinable elements."""
        factors = {
            "emotional_intensity": abs(sentiment['polarity']),
            "positivity_index": sentiment.get('positive', 0),
            "negativity_index": sentiment.get('negative', 0),
            "neutrality_index": sentiment.get('neutral', 0),
            "confidence": np.clip(sentiment.get('score', 1), 0, 1)  # For transformer models with score
        }
        return factors

    def _sequence_distribution(self, sentiment_result):
        """Add sentiment result to sequencer for distribution over time."""
        self.sequenced_results.append(sentiment_result)
        if len(self.sequenced_results) > 5:  # Limit sequence to last 5 results for trend analysis
            self.sequenced_results.pop(0)
        # Calculate average sentiment in sequencer for trend
        avg_sentiment = np.mean([result['polarity'] for result in self.sequenced_results])
        return {"sequenced_avg_sentiment": avg_sentiment, "sequence": self.sequenced_results}

    def set_method(self, method):
        """Dynamically set the sentiment analysis method."""
        self.method = method
        if method == 'vader':
            self.vader_analyzer = SentimentIntensityAnalyzer()
        elif method == 'transformer':
            self.transformer_analyzer = pipeline("sentiment-analysis")
        logging.info(f"Sentiment analysis method set to {method}")

    def set_language(self, language):
        """Set the default language for analysis."""
        self.language = language
        logging.info(f"Language set to {language}")
