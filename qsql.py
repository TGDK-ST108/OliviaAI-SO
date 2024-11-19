import os
import pyodbc
import logging
import yaml
from functools import reduce
from flask import Flask, request, jsonify, session, redirect, url_for
from authlib.integrations.flask_client import OAuth
from azure.identity import AzureCliCredential, DefaultAzureCredential
from qiskit import QuantumCircuit, transpile, assemble
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
from pathlib import Path
import asyncio
import aiosqlite
import zlib
import base64
from datetime import datetime
import hashlib
from dotenv import load_dotenv
import aiosqlite
from cryptography.fernet import Fernet
from azure.keyvault.secrets import SecretClient
from azure.quantum import Workspace
import mitmproxy

load_dotenv()

ws = Workspace(
    subscription_id="your_subscription_id",
    resource_group="your_resource_group",
    name="your_workspace_name",
    location="your_workspace_location"
)
print("Workspace loaded:", ws.name)


# Initialize logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Load configuration from YAML file
try:
    with open("config.yaml", "r") as f:
        config = yaml.safe_load(f)
except FileNotFoundError:
    logger.error("Configuration file 'config.yaml' not found.")
    raise
except yaml.YAMLError as e:
    logger.error(f"Error reading the configuration file: {e}")
    raise

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = config['flask'].get('secret_key', os.environ.get('FLASK_SECRET_KEY'))


# Utility function to initialize Azure Quantum Workspace
def initialize_workspace(credential):
    try:
        workspace = Workspace(
            subscription_id=config["quantum_workspace"]["subscription_id"],
            resource_group=config["quantum_workspace"]["resource_group"],
            name=config["quantum_workspace"]["workspace_name"],
            location=config["quantum_workspace"]["workspace_location"],
            credential=credential
        )
        logger.info("Connected to Azure Quantum workspace successfully.")
        return workspace
    except Exception as e:
        logger.error(f"Failed to connect to Azure Quantum workspace: {e}")
        raise

# Use Azure CLI credentials for initial authentication, fallback to DefaultAzureCredential
try:
    credential = AzureCliCredential()
    workspace = initialize_workspace(credential)
except Exception as e:
    logger.warning("Azure CLI Credential failed, attempting DefaultAzureCredential.")
    credential = DefaultAzureCredential()
    workspace = initialize_workspace(credential)

class QSQL:
    """Manages Azure SQL Database connections and operations."""

    def __init__(self, config):
        """
        Initializes the AzureSQLManager instance.
        
        Parameters:
        - config (dict): Configuration dictionary containing Azure SQL connection details.
        """
        self.connection_string = config.get('azure_sql', {}).get('connection_string')
        if not self.connection_string:
            raise ValueError("Azure SQL connection string not found in the configuration.")
        
        self.connection = None
        self.logger = logging.getLogger(self.__class__.__name__)

    def open_connection(self):
        """Opens a connection to the Azure SQL Database."""
        try:
            self.connection = pyodbc.connect(self.connection_string, timeout=10)
            self.logger.info("Connection to Azure SQL Database opened successfully.")
        except pyodbc.Error as e:
            self.logger.error(f"Failed to connect to Azure SQL Database: {e}")
            raise

    def close_connection(self):
        """Closes the connection to the Azure SQL Database."""
        if self.connection:
            try:
                self.connection.close()
                self.logger.info("Connection to Azure SQL Database closed successfully.")
            except pyodbc.Error as e:
                self.logger.error(f"Error while closing the Azure SQL Database connection: {e}")
                raise
        else:
            self.logger.warning("Attempted to close a connection that was not open.")

    def execute_query(self, query, params=None):
        """
        Executes a SQL query and returns the result.

        Parameters:
        - query (str): The SQL query to be executed.
        - params (tuple or list, optional): Parameters to pass to the query.

        Returns:
        - list: The result of the query as a list of rows.
        """
        if not self.connection:
            self.logger.warning("Connection is not open. Opening connection.")
            self.open_connection()

        try:
            cursor = self.connection.cursor()
            self.logger.info(f"Executing query: {query}")
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)

            rows = cursor.fetchall()
            self.logger.info(f"Query executed successfully. Number of rows fetched: {len(rows)}")
            return rows
        except pyodbc.Error as e:
            self.logger.error(f"Failed to execute query: {e}")
            raise
        finally:
            cursor.close()

    def execute_non_query(self, query, params=None):
        """
        Executes a non-query SQL command (e.g., INSERT, UPDATE, DELETE).

        Parameters:
        - query (str): The SQL command to be executed.
        - params (tuple or list, optional): Parameters to pass to the command.

        Returns:
        - int: Number of rows affected.
        """
        if not self.connection:
            self.logger.warning("Connection is not open. Opening connection.")
            self.open_connection()

        try:
            cursor = self.connection.cursor()
            self.logger.info(f"Executing non-query: {query}")
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)

            self.connection.commit()
            affected_rows = cursor.rowcount
            self.logger.info(f"Non-query executed successfully. Rows affected: {affected_rows}")
            return affected_rows
        except pyodbc.Error as e:
            self.logger.error(f"Failed to execute non-query: {e}")
            self.connection.rollback()
            raise
        finally:
            cursor.close()

    def __enter__(self):
        """Enables the use of AzureSQLManager with a context manager."""
        self.open_connection()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Ensures the connection is properly closed when used with a context manager."""
        self.close_connection()

# Quomo Class for Quantum-Enhanced Memory System
class Quomo:
    """
    Quomo is a quantum-enhanced memory system that securely stores and retrieves data using
    quantum computing principles, encryption, and asynchronous database operations.
    """
    def __init__(self, database_name="memory_database.qo", key_vault_uri=None, secret_name=None, backend_name='aer_simulator'):
        self.database_name = database_name
        self.key_vault_uri = key_vault_uri
        self.secret_name = secret_name
        self.backend_name = backend_name

        # Setup encryption
        self._setup_encryption()

        # Initialize quantum backend
        self.quantum_backend = self._initialize_quantum_backend()

        # Initialize asynchronous database connection
        asyncio.run(self._connect_db())

    def _setup_encryption(self):
        """Sets up encryption using keys from Azure Key Vault."""
        if not self.key_vault_uri or not self.secret_name:
            logger.error("Key Vault URI and Secret Name must be provided for encryption.")
            raise ValueError("Key Vault URI and Secret Name are required.")

        try:
            credential = DefaultAzureCredential()
            client = SecretClient(vault_url=self.key_vault_uri, credential=credential)
            secret = client.get_secret(self.secret_name)
            key = secret.value
            self.cipher_suite = Fernet(key.encode())
            logger.info("Encryption setup successfully.")
        except Exception as e:
            logger.error(f"Encryption setup failed: {e}")
            raise

    def _initialize_quantum_backend(self):
        """Initializes the quantum backend using Qiskit's AerSimulator."""
        try:
            backend = AerSimulator() if self.backend_name == 'aer_simulator' else AerSimulator()
            logger.info(f"Quantum backend '{self.backend_name}' initialized.")
            return backend
        except Exception as e:
            logger.error(f"Failed to initialize quantum backend: {e}")
            raise

    async def _connect_db(self):
        """Asynchronously connects to the SQLite database and ensures the necessary table exists."""
        try:
            self.conn = await aiosqlite.connect(self.database_name)
            self.cursor = await self.conn.cursor()
            await self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS memory_data (
                    interaction_id TEXT PRIMARY KEY,
                    compressed_data TEXT,
                    timestamp TEXT,
                    data_hash TEXT
                )
            ''')
            await self.conn.commit()
            logger.info("Asynchronous database connected and table ensured.")
        except aiosqlite.Error as e:
            logger.error(f"Database connection failed: {e}")
            raise

    def encode_quantum_data(self, data: str) -> str:
        """Quantum-enhanced encoding method using Qiskit."""
        try:
            data_binary = ''.join(format(ord(char), '08b') for char in data)
            num_qubits = len(data_binary)
            qc = QuantumCircuit(num_qubits, num_qubits)
            for i, bit in enumerate(data_binary):
                if bit == '1':
                    qc.x(i)
            if num_qubits > 1:
                qc.h(0)
                for i in range(1, num_qubits):
                    qc.cx(0, i)
            qc.measure(range(num_qubits), range(num_qubits))
            job = execute(qc, backend=self.quantum_backend, shots=1)
            result = job.result()
            counts = result.get_counts()
            measured_bits = list(counts.keys())[0]
            quantum_encoded_data = measured_bits
            compressed_data = zlib.compress(quantum_encoded_data.encode('utf-8'))
            encrypted_data = self.cipher_suite.encrypt(compressed_data)
            encoded_data = base64.b64encode(encrypted_data).decode('utf-8')
            logger.debug("Data encoded and encrypted successfully.")
            return encoded_data
        except Exception as e:
            logger.error(f"Error in quantum data encoding: {e}")
            raise

    def decode_quantum_data(self, encoded_data: str) -> str:
        """Decompress and decode quantum-enhanced data."""
        try:
            encrypted_data = base64.b64decode(encoded_data)
            compressed_data = self.cipher_suite.decrypt(encrypted_data)
            quantum_encoded_data = zlib.decompress(compressed_data).decode('utf-8')
            chars = [chr(int(quantum_encoded_data[i:i+8], 2)) for i in range(0, len(quantum_encoded_data), 8)]
            original_data = ''.join(chars)
            logger.debug("Data decrypted and decompressed successfully.")
            return original_data
        except Exception as e:
            logger.error(f"Error in quantum data decoding: {e}")
            raise

    async def save_interaction(self, interaction_id: str, data: str):
        """Compresses, encrypts, and saves data into the Quomo database asynchronously."""
        try:
            encoded_data = self.encode_quantum_data(data)
            timestamp = datetime.utcnow().isoformat()
            data_hash = hashlib.sha256(base64.b64decode(encoded_data)).hexdigest()
            await self.cursor.execute('''
                INSERT OR REPLACE INTO memory_data (interaction_id, compressed_data, timestamp, data_hash)
                VALUES (?, ?, ?, ?)
            ''', (interaction_id, encoded_data, timestamp, data_hash))
            await self.conn.commit()
            logger.info(f"Data successfully saved for interaction_id: {interaction_id}")
        except aiosqlite.Error as e:
            logger.error(f"Database error while saving interaction {interaction_id}: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error while saving interaction {interaction_id}: {e}")
            raise

    async def retrieve_interaction(self, interaction_id: str) -> str:
        """Retrieves and decompresses data from the Quomo database asynchronously."""
        try:
            async with self.conn.execute('''
                SELECT compressed_data, data_hash FROM memory_data WHERE interaction_id = ?
            ''', (interaction_id,)) as cursor:
                result = await cursor.fetchone()
            if result:
                encoded_data, stored_hash = result
                current_hash = hashlib.sha256(base64.b64decode(encoded_data)).hexdigest()
                if current_hash != stored_hash:
                    logger.warning(f"Data integrity check failed for interaction_id: {interaction_id}")
                    return None
                data = self.decode_quantum_data(encoded_data)
                logger.info(f"Data retrieved and verified for interaction_id: {interaction_id}")
                return data
            else:
                logger.warning(f"No data found for interaction_id: {interaction_id}")
                return None
        except aiosqlite.Error as e:
            logger.error(f"Database error while retrieving interaction {interaction_id}: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error while retrieving interaction {interaction_id}: {e}")
            raise

    async def close(self):
        """Closes the asynchronous database connection."""
        try:
            await self.conn.close()
            logger.info("Asynchronous database connection closed.")
        except Exception as e:
            logger.error(f"Error closing database connection: {e}")
            raise

# Flask Routes
@app.route('/login/microsoft')
def login_microsoft():
    return oauth.microsoft.authorize_redirect(url_for('microsoft_auth_callback', _external=True))

@app.route('/auth/microsoft/callback')
def microsoft_auth_callback():
    try:
        token = oauth.microsoft.authorize_access_token()
        user_info = oauth.microsoft.parse_id_token(token)
        session['user'] = user_info
        return redirect(url_for('profile'))
    except Exception as e:
        logger.error(f"Microsoft OAuth failed: {e}")
        return "Authentication failed. Please try again.", 401

@app.route('/profile')
def profile():
    user = session.get('user')
    if user:
        return f"Logged in as: {user['name']} ({user['preferred_username']})"
    else:
        return "You are not logged in."

@app.route('/')
def index():
    return "Microsoft OAuth with Flask and YAML configuration."

# Main execution
if __name__ == "__main__":
    try:
        app.run(debug=True)
    except Exception as e:
        logger.exception("An error occurred while running the Flask application.")
