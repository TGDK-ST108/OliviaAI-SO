import threading
import logging
import multiprocessing

class ConcurrencyControl:
    def __init__(self, max_concurrent_tasks=None):
        """
        Initialize ConcurrencyControl with a limit on concurrent tasks.
        
        :param max_concurrent_tasks: Optional maximum number of concurrent tasks. 
                                     Defaults to the number of CPU cores if not specified.
        """
        # If max_concurrent_tasks isn't provided, use the number of CPU cores
        self.max_concurrent_tasks = max_concurrent_tasks or multiprocessing.cpu_count()
        self.semaphore = threading.Semaphore(self.max_concurrent_tasks)  # Limit concurrent access
        self.lock = threading.Lock()
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        logging.info(f"ConcurrencyControl initialized with max_concurrent_tasks={self.max_concurrent_tasks}")

    def access_resource(self, resource_id):
        """Access a shared resource with concurrency control."""
        logging.info(f"{threading.current_thread().name} attempting to access resource {resource_id}.")

        # Acquire the semaphore to enforce max concurrent tasks limit
        with self.semaphore:
            logging.info(f"{threading.current_thread().name} acquired access to resource {resource_id}.")
            # If exclusive access is needed within the semaphore-limited section, use a lock
            with self.lock:
                self.simulate_resource_usage(resource_id)
            logging.info(f"{threading.current_thread().name} released access to resource {resource_id}.")

    def simulate_resource_usage(self, resource_id):
        """Simulate some resource usage."""
        logging.info(f"Using resource {resource_id}...")
        threading.Event().wait(2)  # Simulate work with a 2-second wait

# Example usage:
def worker(concurrency_control, resource_id):
    """Worker function to simulate concurrent access."""
    concurrency_control.access_resource(resource_id)

if __name__ == "__main__":
    # Initialize ConcurrencyControl without specifying max_concurrent_tasks (defaults to CPU count)
    concurrency_control = ConcurrencyControl()

    # Create a list of threads to simulate concurrent access
    threads = []
    for i in range(10):  # Adjust the range as needed for testing
        thread = threading.Thread(target=worker, args=(concurrency_control, f"Resource-{i}"), name=f"Thread-{i}")
        threads.append(thread)
        thread.start()

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

    logging.info("All threads have completed.")
