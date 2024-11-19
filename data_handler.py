class DataHandler:
    def __init__(self):
        """Initialize the DataHandler."""
        self.data_store = []  # or connect to an actual data source
    
    def add_data(self, data):
        """
        Add data to the storage.

        Args:
            data (any): The data to be added to storage.
        """
        self.data_storage.append(data)
        print("Data added to storage.")

    def process_data(self):
        """
        Process stored data.
        
        This method can be customized to perform any operations on the stored data.
        """
        processed_data = [self._process_single_data(d) for d in self.data_storage]
        print("Data processed successfully.")
        return processed_data

    def _process_single_data(self, data):
        """A placeholder for individual data processing logic."""
        # Implement your processing logic here
        return data  # Returning data as-is for this example

    def display_data(self):
        """Display all stored data."""
        for i, data in enumerate(self.data_storage):
            print(f"Data {i}: {data}")

    def retrieve_recent_data(self):
        """Fetch the most recent data entry."""
        if self.data_store:
            return self.data_store[-1]  # Return the latest item
        logging.warning("Data store is empty; no recent data to retrieve.")
        return None
