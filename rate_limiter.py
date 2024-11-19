import time
import logging

class RateLimiter:
    def __init__(self, rate_limit, per):
        """
        Initialize the RateLimiter.

        :param rate_limit: Number of allowed requests.
        :param per: Time window (in seconds) for the rate limit.
        """
        self.rate_limit = rate_limit
        self.per = per
        self.requests = []
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    def is_allowed(self):
        """Check if a new request is allowed based on the rate limit."""
        current_time = time.time()

        # Remove requests that are outside the time window
        self.requests = [timestamp for timestamp in self.requests if timestamp > current_time - self.per]

        if len(self.requests) < self.rate_limit:
            self.requests.append(current_time)
            logging.info("Request allowed.")
            return True
        else:
            logging.warning("Rate limit exceeded. Request denied.")
            return False

    def reset(self):
        """Reset the request history."""
        self.requests.clear()
        logging.info("Rate limiter reset.")

# Example usage:
if __name__ == "__main__":
    rate_limiter = RateLimiter(rate_limit=5, per=10)  # Allow 5 requests every 10 seconds

    # Simulate making requests
    for i in range(10):
        if rate_limiter.is_allowed():
            print(f"Request {i + 1} processed.")
        else:
            print(f"Request {i + 1} denied.")
        time.sleep(1)  # Simulate a 1-second interval between requests
