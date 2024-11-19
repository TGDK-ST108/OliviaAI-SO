import logging
import psutil  # You may need to install this package via pip

class DynamicResourceAllocator:
    def __init__(self, initial_resources=None):
        """
        Initialize the Dynamic Resource Allocator with optional initial resources.
        If no initial resources are provided, dynamically allocate based on hardware.

        :param initial_resources: Dictionary of initial resources to allocate.
        """
        self.resources = initial_resources if initial_resources else self.get_dynamic_resources()
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

        for resource_id, amount in self.resources.items():
            logging.info(f"Initialized resource '{resource_id}' with {amount} allocated.")

    def get_dynamic_resources(self):
        """Retrieve system hardware resources dynamically."""
        dynamic_resources = {
            'CPU': psutil.cpu_count(logical=True),  # Logical cores
            'Memory': round(psutil.virtual_memory().available / (1024 ** 3), 2),  # Available memory in GB
            'Disk': round(psutil.disk_usage('/').free / (1024 ** 3), 2)  # Free disk space in GB
        }
        logging.info(f"Dynamically allocated resources based on hardware: {dynamic_resources}")
        return dynamic_resources

    def allocate(self, resource_id, amount):
        """Allocate a specified amount of a resource."""
        if resource_id in self.resources:
            self.resources[resource_id] += amount
            logging.info(f"Allocated {amount} of resource '{resource_id}'. Total: {self.resources[resource_id]}")
        else:
            self.resources[resource_id] = amount
            logging.info(f"Created and allocated {amount} of resource '{resource_id}'.")

    def deallocate(self, resource_id, amount):
        """Deallocate a specified amount of a resource."""
        if resource_id in self.resources:
            if self.resources[resource_id] >= amount:
                self.resources[resource_id] -= amount
                logging.info(f"Deallocated {amount} of resource '{resource_id}'. Remaining: {self.resources[resource_id]}")
                if self.resources[resource_id] == 0:
                    del self.resources[resource_id]  # Remove resource if fully deallocated
                    logging.info(f"Resource '{resource_id}' fully deallocated and removed.")
            else:
                logging.warning(f"Cannot deallocate {amount} of resource '{resource_id}'; only {self.resources[resource_id]} available.")
        else:
            logging.warning(f"Resource '{resource_id}' not found for deallocation.")

    def get_resource_status(self, resource_id):
        """Get the current status of a specified resource."""
        if resource_id in self.resources:
            status = self.resources[resource_id]
            logging.info(f"Resource '{resource_id}' has {status} allocated.")
            return status
        else:
            logging.info(f"Resource '{resource_id}' not found.")
            return 0

    def list_resources(self):
        """List all resources and their allocated amounts."""
        logging.info("Current resources:")
        for resource_id, amount in self.resources.items():
            logging.info(f" - {resource_id}: {amount}")

# Example usage:
if __name__ == "__main__":
    allocator = DynamicResourceAllocator()  # Uses dynamic hardware-based allocation

    # List initial resources based on hardware capacity
    allocator.list_resources()

    # Allocate more resources as needed
    allocator.allocate('CPU', 2)
    allocator.allocate('GPU', 1)  # Assuming a system with available GPUs

    # List resources after additional allocations
    allocator.list_resources()

    # Deallocate resources
    allocator.deallocate('Memory', 1)  # Free 1 GB of memory
    allocator.deallocate('Disk', 5)    # Free 5 GB of disk

    # Check resource status
    allocator.get_resource_status('CPU')
    allocator.get_resource_status('Memory')

    # Final list of resources
    allocator.list_resources()
