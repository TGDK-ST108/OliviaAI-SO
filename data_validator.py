# data_validator.py

import pandas as pd
import logging

class DataValidator:
    def __init__(self):
        pass

    def validate(self, data: pd.DataFrame) -> bool:
        """
        Validate the data.

        Criteria:
        - Data is a pandas DataFrame
        - No missing values
        - Required columns are present
        - Data types are correct
        """
        logging.info("Starting data validation.")

        # Check if data is a DataFrame
        if not isinstance(data, pd.DataFrame):
            logging.error("Data is not a pandas DataFrame.")
            return False

        # Check for missing values
        if data.isnull().values.any():
            logging.error("Data contains missing values.")
            return False

        # Define required columns and their types
        required_columns = {
            'sensor_value': (pd.np.float64, pd.np.float32, float),
            'timestamp': (pd.Timestamp, str)
        }

        for column, expected_types in required_columns.items():
            if column not in data.columns:
                logging.error(f"Missing required column: {column}")
                return False
            if not all(isinstance(val, expected_types) for val in data[column]):
                logging.error(f"Incorrect data type in column: {column}")
                return False

        logging.info("Data validation successful.")
        return True
