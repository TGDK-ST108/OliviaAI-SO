class Quoma:
    def __init__(self, connection_string):
        """
        Initialize the database connection.
        """
        self.connection_string = connection_string
        self.database = {}

    def query(self, sql_query):
        """
        Simulate querying data from the database.
        """
        print(f"Executing query: {sql_query}")
        return [[1/7, 2], [2/3, 4], [4/5, 6]]  # Mock result

    def save(self, table_name, data):
        """
        Simulate saving data to the database.
        """
        self.database[table_name] = data
        print(f"Data saved to table '{table_name}': {data}")

def connect(connection_string):
    """
    Connect to the database using the provided connection string.
    """
    return Quoma(connection_string)

