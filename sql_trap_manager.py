import logging
import sqlite3

class SQLTrapManager:
    def __init__(self, db_path):
        self.connection = sqlite3.connect(db_path)
        self.cursor = self.connection.cursor()
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    def execute_query(self, query, params=None):
        """Execute a SQL query with parameterized inputs to prevent SQL injection."""
        if self.is_suspicious_query(query):
            logging.warning(f"Suspicious query detected: {query}")
            return None

        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)

            self.connection.commit()
            logging.info(f"Executed query: {query} with params: {params}")
        except sqlite3.Error as e:
            logging.error(f"Error executing query: {e}")
            return None

    def fetch_query(self, query, params=None):
        """Fetch results from a SQL query."""
        if self.is_suspicious_query(query):
            logging.warning(f"Suspicious query detected: {query}")
            return None

        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)

            results = self.cursor.fetchall()
            logging.info(f"Fetched results for query: {query} with params: {params}")
            return results
        except sqlite3.Error as e:
            logging.error(f"Error fetching query: {e}")
            return None

    def is_suspicious_query(self, query):
        """Basic check for suspicious queries (e.g., DROP, DELETE without WHERE)."""
        # This is a very basic check and should be expanded for production use
        suspicious_keywords = ['DROP', 'DELETE', '--', ';']
        return any(keyword in query.upper() for keyword in suspicious_keywords)

    def close(self):
        """Close the database connection."""
        self.cursor.close()
        self.connection.close()
        logging.info("Closed database connection.")

# Example usage:
if __name__ == "__main__":
    db_path = 'example.db'
    sql_trap_manager = SQLTrapManager(db_path)

    # Create a table
    sql_trap_manager.execute_query("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT)")

    # Insert a user
    sql_trap_manager.execute_query("INSERT INTO users (name) VALUES (?)", ("Alice",))

    # Fetch users
    users = sql_trap_manager.fetch_query("SELECT * FROM users")
    print("Users:", users)

    # Close the manager
    sql_trap_manager.close()
