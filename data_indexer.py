class DataIndexer:
    def __init__(self):
        """Initialize the DataIndexer."""
        self.index = {}
    
    def index_data(self, data):
        """
        Index the given data.

        Args:
            data (dict): A dictionary of data to be indexed.
        """
        for key, value in data.items():
            self.index[key] = value
        print("Data indexed successfully.")

    def retrieve(self, key):
        """
        Retrieve indexed data by key.

        Args:
            key (str): The key for the indexed data.

        Returns:
            The value associated with the key, or None if not found.
        """
        return self.index.get(key, None)

    def display_index(self):
        """Display the current index."""
        for key, value in self.index.items():
            print(f"Key: {key}, Value: {value}")
