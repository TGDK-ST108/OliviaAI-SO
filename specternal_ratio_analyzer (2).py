import numpy as np
import logging

class SpecternalRatioAnalyzer:
    def __init__(self):
        logging.info("SpecternalRatioAnalyzer initialized.")

    def calculate_specternal_ratios(self, data):
        """Calculate specternal ratios of a numerical dataset."""
        if len(data) < 2:
            raise ValueError("Data must contain at least two points to calculate ratios.")
        
        # Calculate first-order differences
        differences = np.diff(data)
        
        # Calculate specternal ratios
        ratios = np.divide(differences[1:], differences[:-1], out=np.zeros_like(differences[1:]), where=differences[:-1] != 0)
        
        logging.info("Calculated specternal ratios: {}".format(ratios))
        return ratios

    def analyze_data(self, data):
        """Perform analysis on the given data."""
        ratios = self.calculate_specternal_ratios(data)
        analysis_result = {
            "ratios": ratios,
            "mean_ratio": np.mean(ratios),
            "std_dev_ratio": np.std(ratios),
            "max_ratio": np.max(ratios),
            "min_ratio": np.min(ratios)
        }
        logging.info("Specternal data analysis result: {}".format(analysis_result))
        return analysis_result

# Example usage:
if __name__ == '__main__':
    analyzer = SpecternalRatioAnalyzer()
    data = [1, 3, 2, 8, 5, 12]
    
    try:
        analysis_results = analyzer.analyze_data(data)
        print("Specternal Analysis Results:", analysis_results)
    except ValueError as e:
        print(f"Error: {e}")