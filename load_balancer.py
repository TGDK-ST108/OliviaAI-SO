import logging
import random

class LoadBalancer:
    def __init__(self, servers):
        self.servers = servers
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    def get_server(self):
        """Randomly select a server to distribute the load."""
        selected_server = random.choice(self.servers)
        logging.info(f"Selected server: {selected_server}")
        return selected_server

    def distribute_request(self, request):
        """Distribute a request to one of the available servers."""
        server = self.get_server()
        # Simulate sending the request to the server
        response = self.send_request_to_server(server, request)
        return response

    def send_request_to_server(self, server, request):
        """Simulate sending a request to a server."""
        logging.info(f"Sending request '{request}' to server '{server}'")
        # In a real-world scenario, this could involve network calls, etc.
        response = f"Response from {server} for request '{request}'"
        return response

# Example usage:
if __name__ == "__main__":
    servers = ["Server1", "Server2", "Server3"]
    load_balancer = LoadBalancer(servers)

    # Simulate distributing requests
    requests = ["Request A", "Request B", "Request C"]
    for req in requests:
        response = load_balancer.distribute_request(req)
        print(response)
