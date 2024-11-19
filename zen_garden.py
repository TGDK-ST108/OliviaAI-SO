import numpy as np
import logging
import matplotlib.pyplot as plt
from datetime import datetime
from mahadevi import Mahadevi
from Maharaga import Maharaga

       

class ZenGarden:
    def __init__(self, mahadevi, maharaga, frequency=1.0):
        """
        Initialize ZenGarden with Mahadevi and Maharaga for vector and spatial transformations.
        """
        self.frequency = frequency
        self.mahadevi = mahadevi
        self.maharaga = maharaga
        self.contextual_vectors = []
        self.transformations = []    # Post-processing functions
        self.preprocessors = []      # Pre-processing functions
        self.vector_flows = []       # Vector flows
        self.logs = []  # Store logs for visualization
        logging.info("ZenGarden initialized with Mahadevi and Maharaga.")

    def add_log(self, log_entry):
        """
        Add a log entry for tracking performance and transformation steps.
        """
        self.logs.append(log_entry)
        logging.debug(f"Log added: {log_entry}")

    def clean_numeric_data(self, data):
        """
        Recursively clean the data structure to include only numeric values.
        Converts date/time strings to timestamps if detected.
        """
        if isinstance(data, (list, tuple)):
            cleaned = []
            for item in data:
                cleaned_item = self.clean_numeric_data(item)
                if cleaned_item is not None:
                    cleaned.append(cleaned_item)
            return cleaned if cleaned else None
        elif isinstance(data, dict):
            cleaned = []
            for value in data.values():
                cleaned_value = self.clean_numeric_data(value)
                if cleaned_value is not None:
                    cleaned.append(cleaned_value)
            return cleaned if cleaned else None
        elif isinstance(data, (int, float, np.number)):
            return data
        elif isinstance(data, str):
            # Attempt to parse the string as a date/time
            try:
                dt = self.parse_datetime_string(data)
                if dt is not None:
                    timestamp = dt.timestamp()
                    return timestamp
                else:
                    return None
            except Exception:
                return None
        else:
            # Non-numeric data is excluded
            return None

    # Methods to add custom processing functions
    def add_transformation(self, transformation_fn):
        """
        Add a custom transformation function (post-processing) that utilizes Mahadevi's operations.
        """
        self.transformations.append(transformation_fn)
        logging.info("Transformation function added to ZenGarden.")

    def add_preprocessor(self, preprocessor_fn):
        """
        Add a custom preprocessor function (pre-processing) that prepares data for Mahadevi's operations.
        """
        self.preprocessors.append(preprocessor_fn)
        logging.info("Preprocessor function added to ZenGarden.")

    def add_vector_flow(self, vector_field):
        """
        Create a vector flow by setting up a vector field using Mahadevi's vector operations.
        """
        self.mahadevi.set_vector_field(vector_field)
        self.vector_flows.append(vector_field)
        logging.info("Vector flow added to ZenGarden.")

    # Methods to apply processing functions
    def apply_preprocessors(self, data):
        """
        Apply pre-processing transformations to data using the registered preprocessor functions.
        """
        for preprocessor in self.preprocessors:
            data = preprocessor(data)
            logging.debug(f"Preprocessor applied, data shape: {np.shape(data)}")
        return data

    def apply_transformations(self, data):
        """
        Apply post-processing transformations to data using the registered transformation functions.
        """
        for transformation in self.transformations:
            data = transformation(data)
            logging.debug(f"Transformation applied, data shape: {np.shape(data)}")
        return data

    # Core methods utilizing Mahadevi's functionality
    def adjust_variable_grade(self, data):
        """
        Use Mahadevi to adjust data by normalizing and scaling according to the central frequency.
        """
        adjusted_data = []
        for vector in data:
            norm_vector = self.mahadevi.normalize_vector(np.array(vector))
            adjusted_vector = self.mahadevi.scalar_multiply(norm_vector, self.frequency)
            adjusted_data.append(adjusted_vector)
        logging.info("Data adjusted using Mahadevi's vector operations.")
        return adjusted_data

    def generate_vector_field(self, data):
        """
        Generate a vector field based on input data using Mahadevi's vector generation methods.
        """
        preprocessed_data = self.apply_preprocessors(data)
        vector_field = [self.mahadevi.generate_random_vector(len(preprocessed_data)) for _ in preprocessed_data]
        logging.info(f"Generated vector field with Mahadevi of length {len(vector_field)}.")
        return vector_field

    def create_antivector_field(self, vector_field):
        """
        Generate an antivector field, the inverse of a given vector field, using Mahadevi's operations.
        """
        antivector_field = [self.mahadevi.scalar_multiply(vector, -1) for vector in vector_field]
        logging.info("Generated antivector field.")
        return antivector_field

    def coherence_transform(self, data):
        """
        Apply coherence transformations using Mahadevi to balance the user relationship with the environment,
        based on vector coherence and Mahadevi’s operations.
        """
        coherence_vectors = [self.mahadevi.normalize_vector(vector) for vector in data]
        transformed_data = [self.mahadevi.multiply_vectors(vector, coherence_vector)
                            for vector, coherence_vector in zip(data, coherence_vectors)]
        logging.debug("Coherence transformation applied to data.")
        return transformed_data

    def run_determination_sequence(self, data):
        try:
            # Preprocess data
            data = self.apply_preprocessors(data)
            logging.debug(f"Data after preprocessing: {data}")

            # Clean data to include only numeric elements and convert date/time strings
            data = self.clean_numeric_data(data)
            logging.debug(f"Data after cleaning: {data}")

            if not data:
                logging.warning("Data contains no numeric or date/time values after cleaning.")
                return None  # Or provide a default value or behavior

            # Ensure data is a list of numpy arrays
            data = [np.array(vector, dtype=float) for vector in data]

            # Apply coherence transformation to data
            coherent_data = self.coherence_transform(data)

            # Apply post-processing transformations
            processed_data = self.apply_transformations(coherent_data)
            logging.info("Determination sequence completed with processed data.")
            return processed_data
        except Exception as e:
            logging.error(f"Error in determination sequence: {e}")
            raise TypeError(f"Data format incompatible for transformation. Ensure numerical or date/time data. Details: {e}")

    def generative_flow_transform(self, data):
        """
        Apply a generative flow transformation based on user-defined vector flows and Mahadevi’s vector operations.
        """
        # Pre-process data
        data = self.apply_preprocessors(data)

        # Generate the vector field
        vector_field = self.generate_vector_field(data)

        # Apply coherence transformations
        coherence_transformed = self.coherence_transform(vector_field)

        # Introduce vector flows if present
        for flow in self.vector_flows:
            coherence_transformed = [self.mahadevi.add_vectors(vector, flow_vector)
                                     for vector, flow_vector in zip(coherence_transformed, flow)]
            logging.debug("Vector flow applied within generative transformation.")

        # Apply post-processing transformations
        generative_data = self.apply_transformations(coherence_transformed)
        logging.info("Generative flow transformation completed.")
        return generative_data

    def execute_custom_interaction(self, user_data, custom_processing_fn):
        """
        Allows custom interactions by processing user data through a specified function
        that depends on Mahadevi's vector operations.
        """
        # Pre-process data
        user_data = self.apply_preprocessors(user_data)

        # Run custom processing using Mahadevi's methods
        processed_data = custom_processing_fn(user_data)

        # Apply post-processing transformations
        final_output = self.apply_transformations(processed_data)
        logging.info("Custom interaction executed.")
        return final_output

    def display_waveform(self, data, title="ZenGarden Waveform"):
        """
        Display data as a waveform, showing generative and transformed states,
        utilizing Mahadevi's vector operations for visualization.
        """
        time = np.linspace(0, len(data), len(data))
        signal = np.sin(2 * np.pi * self.frequency * time) * np.array(data)
        plt.plot(time, signal)
        plt.title(title)
        plt.xlabel("Time")
        plt.ylabel("Amplitude")
        plt.show()
        logging.info("Waveform display rendered.")

    def compute_geometric_centrality(self):
        """
        Use Mahadevi to calculate the centroid of all vectors in contextual_vectors.
        """
        if not self.contextual_vectors:
            raise ValueError("No vectors available in contextual_vectors.")

        centroid = self.mahadevi.compute_centroid(self.contextual_vectors)
        logging.info(f"Computed centroid: {centroid}")
        return centroid

    def apply_centrality_adjustment(self, data):
        """
        Adjust each vector in data based on the computed centroid using Mahadevi's vector operations.
        """
        centroid = self.compute_geometric_centrality()
        adjusted_data = [self.mahadevi.add_vectors(vector, centroid) for vector in data]
        logging.info("Centrality adjustment applied to data.")
        return adjusted_data

    def synchronize_vectors_with_frequency(self, data):
        """
        Synchronize vectors in data with the primary frequency using Mahadevi's scalar multiplication.
        """
        adjusted_data = []
        for vector in data:
            adjusted_vector = self.mahadevi.scalar_multiply(vector, self.frequency)
            adjusted_data.append(adjusted_vector)
        logging.info("Vectors synchronized with primary frequency.")
        return adjusted_data

    def visualize_logs(self):
        """
        Generate a line plot for performance logs over time.
        """
        if not self.logs:
            logging.warning("No logs available for visualization.")
            return

        # Extract time and values for visualization
        times = [log['time'] for log in self.logs]
        values = [log['value'] for log in self.logs]

        plt.figure(figsize=(10, 6))
        plt.plot(times, values, marker='o', label="Performance Metric")
        plt.title("Performance Metrics Over Time")
        plt.xlabel("Time")
        plt.ylabel("Value")
        plt.grid()
        plt.legend()
        plt.show()
        logging.info("Logs visualized.")

    def generate_heatmap(self, data, title="Heatmap"):
        """
        Generate a heatmap of the given data.
        """
        plt.figure(figsize=(8, 6))
        plt.imshow(data, cmap='viridis', interpolation='nearest')
        plt.colorbar(label="Intensity")
        plt.title(title)
        plt.xlabel("X-axis")
        plt.ylabel("Y-axis")
        plt.show()
        logging.info("Heatmap generated.")

    def visualize_vector_field(self, vector_field, title="Vector Field"):
        """
        Visualize a vector field using quiver plot.
        """
        plt.figure(figsize=(8, 8))
        X, Y = np.meshgrid(range(len(vector_field)), range(len(vector_field[0])))
        U = np.array([vector[0] for vector in vector_field])
        V = np.array([vector[1] for vector in vector_field])

        plt.quiver(X, Y, U, V, angles='xy', scale_units='xy', scale=1, color="blue")
        plt.title(title)
        plt.xlabel("X-axis")
        plt.ylabel("Y-axis")
        plt.grid()
        plt.show()
        logging.info("Vector field visualized.")

    def plot_waveform(self, data, title="Waveform"):
        """
        Display data as a waveform.
        """
        time = np.linspace(0, len(data), len(data))
        signal = np.sin(2 * np.pi * self.frequency * time) * np.array(data)

        plt.figure(figsize=(10, 6))
        plt.plot(time, signal, label="Waveform")
        plt.title(title)
        plt.xlabel("Time")
        plt.ylabel("Amplitude")
        plt.grid()
        plt.legend()
        plt.show()
        logging.info("Waveform plotted.")

    def analyze_performance(self, data, metric_fn):
        """
        Analyze performance metrics over data and visualize results.
        """
        metrics = [metric_fn(vector) for vector in data]
        self.add_log({"time": len(self.logs), "value": np.mean(metrics)})
        self.visualize_logs()
        logging.info("Performance analysis completed.")
