import numpy as np
import pandas as pd
import logging

# Initialize logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class TulipJam:
    def __init__(self, data_source):
        self.data_source = data_source
        self.data = None
        logging.info(f"TulipJam initialized with data source: {data_source}")

    def load_data(self):
        """Load data from the source."""
        try:
            self.data = pd.read_csv(self.data_source)
            logging.info("Data loaded successfully.")
        except FileNotFoundError:
            logging.error(f"File not found: {self.data_source}")
            self.data = None
        except pd.errors.EmptyDataError:
            logging.error(f"Empty data error: {self.data_source}")
            self.data = None
        except pd.errors.ParserError:
            logging.error(f"Parsing error with file: {self.data_source}")
            self.data = None
        except Exception as e:
            logging.error(f"Failed to load data: {e}")
            self.data = None

    def transform_data(self):
        """Perform transformations on the data."""
        if self.data is not None:
            try:
                numeric_cols = self.data.select_dtypes(include=[np.number]).columns
                self.data[numeric_cols] = (self.data[numeric_cols] - self.data[numeric_cols].mean()) / self.data[numeric_cols].std()
                logging.info("Data transformation complete.")
            except Exception as e:
                logging.error(f"Failed to transform data: {e}")
        else:
            logging.warning("No data to transform.")

    def analyze_data(self):
        """Perform analysis on the transformed data."""
        if self.data is not None:
            try:
                analysis_results = self.data.describe()
                logging.info("Data analysis complete.")
                return analysis_results
            except Exception as e:
                logging.error(f"Failed to analyze data: {e}")
                return None
        else:
            logging.warning("No data to analyze.")
            return None

    def save_results(self, output_file):
        """Save analysis results to a file."""
        results = self.analyze_data()
        if results is not None:
            try:
                results.to_csv(output_file)
                logging.info(f"Results saved to {output_file}.")
            except Exception as e:
                logging.error(f"Failed to save results: {e}")
        else:
            logging.warning("No results to save.")

# Example usage
if __name__ == "__main__":
    tulip_jam = TulipJam(data_source='data.csv')
    tulip_jam.load_data()
    tulip_jam.transform_data()
    tulip_jam.save_results('results.csv')