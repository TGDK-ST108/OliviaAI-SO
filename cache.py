import yaml
import logging
from collections import OrderedDict

# Load YAML configuration
with open('config.yaml', 'r') as f:
    config = yaml.safe_load(f)

class Cache:
    def __init__(self, max_size):
        """
        Initialize the Cache.

        :param max_size: Maximum number of items the cache can hold.
        """
        self.cache = OrderedDict()
        self.max_size = max_size
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    def get(self, key):
        """Retrieve an item from the cache."""
        if key not in self.cache:
            logging.warning(f"Key '{key}' not found in cache.")
            return None
        else:
            # Move the accessed item to the end to maintain LRU order
            self.cache.move_to_end(key)
            logging.info(f"Retrieved '{key}' from cache.")
            return self.cache[key]

    def set(self, key, value):
        """Set an item in the cache."""
        if key in self.cache:
            logging.info(f"Updating key '{key}' in cache.")
            self.cache.move_to_end(key)
        else:
            logging.info(f"Adding key '{key}' to cache.")

        self.cache[key] = value

        # Evict the least recently used item if the cache exceeds the maximum size
        if len(self.cache) > self.max_size:
            evicted_key, evicted_value = self.cache.popitem(last=False)
            logging.warning(f"Cache full. Evicted '{evicted_key}': '{evicted_value}'")

    def remove(self, key):
        """Remove an item from the cache."""
        if key in self.cache:
            removed_value = self.cache.pop(key)
            logging.info(f"Removed '{key}' from cache: '{removed_value}'")
        else:
            logging.warning(f"Key '{key}' not found in cache.")

    def clear(self):
        """Clear all items from the cache."""
        self.cache.clear()
        logging.info("Cache cleared.")


# Example usage
if __name__ == "__main__":
    max_size = config.get('cache', {}).get('max_size', 3)  # Default to 3 if not set in config
    cache = Cache(max_size=max_size)

    # Adding items to the cache
    cache.set('a', 1)
    cache.set('b', 2)
    cache.set('c', 3)

    print(cache.get('a'))  # Output: 1
    cache.set('d', 4)      # This should evict 'b' since it's the LRU
    print(cache.get('b'))  # Output: None (since 'b' was evicted)

    cache.remove('c')      # Remove 'c'
    print(cache.get('c'))  # Output: None

    cache.clear()          # Clear the cache
