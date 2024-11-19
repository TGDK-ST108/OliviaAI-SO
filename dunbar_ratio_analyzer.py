# dunbar_analyzer.py
import numpy as np
import logging
from scipy.stats import skew, kurtosis

class DunbarRatioAnalyzer:
    def __init__(self, threshold=150, dynamic_threshold=False, logger=None):
        self.base_threshold = threshold
        self.dynamic_threshold = dynamic_threshold
        self.logger = logger or logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)

    def analyze_data(self, data):
        # Calculate primary statistical metrics
        mean = np.mean(data)
        std_dev = np.std(data) + 1e-5  # Avoid division by zero
        ratio = mean / std_dev

        # Adjust threshold dynamically based on data variance if enabled
        threshold = self.base_threshold
        if self.dynamic_threshold:
            variance = np.var(data)
            threshold = self.base_threshold * (1 + variance / 100)  # Scale based on variance

        # Determine if the ratio exceeds the threshold
        exceeds_threshold = ratio > threshold

        # Calculate additional metrics for deeper analysis
        data_skewness = skew(data)
        data_kurtosis = kurtosis(data)

        # Log detailed information if a logger is provided
        self.logger.info(f"Mean: {mean}, Std Dev: {std_dev}, Ratio: {ratio}")
        self.logger.info(f"Threshold: {threshold}, Exceeds Threshold: {exceeds_threshold}")
        self.logger.info(f"Skewness: {data_skewness}, Kurtosis: {data_kurtosis}")

        return {
            "ratio": ratio,
            "exceeds_threshold": exceeds_threshold,
            "dynamic_threshold": threshold,
            "skewness": data_skewness,
            "kurtosis": data_kurtosis
        }

    def correlate_countermeasures(self, analysis_results):
        # Provide countermeasures based on the analysis
        if analysis_results['exceeds_threshold']:
            if analysis_results['skewness'] > 1:
                countermeasures = "Implement density reduction and monitor for outliers."
            elif analysis_results['kurtosis'] > 3:
                countermeasures = "Reduce data peaks; consider redistributing."
            else:
                countermeasures = "General density reduction measures recommended."
        else:
            if analysis_results['skewness'] < -1:
                countermeasures = "Increase data spread to balance negative skew."
            else:
                countermeasures = "Density levels are within acceptable range."
        
        self.logger.info(f"Countermeasures: {countermeasures}")
        return countermeasures
