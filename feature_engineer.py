# feature_engineer.py

import pandas as pd
import numpy as np
import logging

class FeatureEngineer:
    def __init__(self):
        pass

    def generate_features(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Generate new features from the existing data.

        Example Features:
        - Rolling mean and standard deviation
        - Time-based features (e.g., hour of day)
        """
        logging.info("Starting feature engineering.")

        # Ensure 'timestamp' is in datetime format
        data['timestamp'] = pd.to_datetime(data['timestamp'])

        # Sort data by timestamp
        data = data.sort_values('timestamp').reset_index(drop=True)

        # Create time-based features
        data['hour'] = data['timestamp'].dt.hour
        data['day_of_week'] = data['timestamp'].dt.dayofweek
        data['month'] = data['timestamp'].dt.month

        # Create rolling statistics
        data['rolling_mean_3'] = data['sensor_value'].rolling(window=3).mean()
        data['rolling_std_3'] = data['sensor_value'].rolling(window=3).std()

        # Fill NaN values resulted from rolling operations
        data.fillna(method='bfill', inplace=True)

        logging.info("Feature engineering completed.")
        return data
