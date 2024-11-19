import psutil
import logging
import time

class ResourceMonitor:
    def __init__(self, interval=5):
        self.interval = interval
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    def monitor_cpu(self):
        """Monitor CPU usage."""
        cpu_usage = psutil.cpu_percent(interval=self.interval)
        logging.info(f"CPU Usage: {cpu_usage}%")

    def monitor_memory(self):
        """Monitor memory usage."""
        memory_info = psutil.virtual_memory()
        memory_usage = memory_info.percent
        logging.info(f"Memory Usage: {memory_usage}% (Total: {memory_info.total / (1024**3):.2f} GB, Available: {memory_info.available / (1024**3):.2f} GB)")

    def monitor_disk(self):
        """Monitor disk usage."""
        disk_info = psutil.disk_usage('/')
        disk_usage = disk_info.percent
        logging.info(f"Disk Usage: {disk_usage}% (Total: {disk_info.total / (1024**3):.2f} GB, Used: {disk_info.used / (1024**3):.2f} GB)")

    def start_monitoring(self):
        """Start monitoring system resources."""
        logging.info("Starting resource monitoring...")
        while True:
            self.monitor_cpu()
            self.monitor_memory()
            self.monitor_disk()
            time.sleep(self.interval)

# Example usage:
if __name__ == "__main__":
    monitor = ResourceMonitor(interval=5)  # Monitor resources every 5 seconds
    monitor.start_monitoring()
