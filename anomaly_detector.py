# anomaly_detector.py

import pandas as pd
import numpy as np
import logging

class AnomalyDetector:
    def __init__(self, threshold: float = 3.0):
        """
        Initialize the anomaly detector.

        :param threshold: Z-score threshold for detecting anomalies.
        """
        self.threshold = threshold

    def detect(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Detect anomalies in the 'sensor_value' column using Z-score.

        :return: DataFrame containing anomalies.
        """
        logging.info("Starting anomaly detection.")

        if 'sensor_value' not in data.columns:
            logging.error("'sensor_value' column not found in data.")
            return pd.DataFrame()

        # Calculate Z-scores
        mean = data['sensor_value'].mean()
        std = data['sensor_value'].std()
        data['z_score'] = (data['sensor_value'] - mean) / std

        # Identify anomalies
        anomalies = data[np.abs(data['z_score']) > self.threshold]

        logging.info(f"Anomaly detection completed. {len(anomalies)} anomalies found.")
        return anomalies[['timestamp', 'sensor_value', 'z_score']]
