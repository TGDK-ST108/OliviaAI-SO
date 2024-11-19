import logging

class PhantomGateHandler:
    def __init__(self):
        logging.info("PhantomGateHandler initialized.")
        # Initialize storage or relevant structures
        self.storage = {}
    
    def store_data(self, data: str) -> str:
        """
        Store data using phantom gate mechanisms.
        
        Parameters:
        - data: The data to store.
        
        Returns:
        - A confirmation message.
        """
        logging.info("Storing data using Phantom Gate Handler.")
        # Example storage
        data_id = str(len(self.storage) + 1)
        self.storage[data_id] = data
        return f"Data stored with ID: {data_id}"
    
    def retrieve_data(self, data_id: str) -> str:
        """
        Retrieve data using its ID.
        
        Parameters:
        - data_id: The ID of the data to retrieve.
        
        Returns:
        - The stored data or an error message if not found.
        """
        logging.info(f"Retrieving data with ID: {data_id}")
        if data_id in self.storage:
            return self.storage[data_id]
        return "Data not found."

# Example usage
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    
    handler = PhantomGateHandler()
    
    # Store and retrieve data
    data_id = handler.store_data("Important data")
    retrieved_data = handler.retrieve_data(data_id.split(': ')[1])
    print("Retrieved Data:", retrieved_data)