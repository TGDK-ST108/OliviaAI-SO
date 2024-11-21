import time
import psutil
import numpy as np
import cupy as cp
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# CPU Test: Measuring CPU usage
def cpu_test(duration=5):
    logger.info(f"Starting CPU performance test for {duration} seconds...")
    start_time = time.time()
    while time.time() - start_time < duration:
        # Simulating CPU load by running a simple computation
        _ = np.random.rand(1000, 1000) @ np.random.rand(1000, 1000)
    cpu_usage = psutil.cpu_percent(interval=1)
    logger.info(f"CPU Usage: {cpu_usage}%")
    return cpu_usage

# GPU Test: Measuring GPU performance (if GPU is available)
def gpu_test(duration=5):
    try:
        # Running a GPU computation using CuPy
        logger.info(f"Starting GPU performance test for {duration} seconds...")
        start_time = time.time()
        while time.time() - start_time < duration:
            x = cp.random.rand(1000, 1000)
            y = cp.random.rand(1000, 1000)
            z = cp.dot(x, y)
        gpu_usage = cp.cuda.Device(0).compute_utilization
        logger.info(f"GPU Usage: {gpu_usage}")
        return gpu_usage
    except Exception as e:
        logger.error(f"GPU test failed: {e}")
        return None

# Memory Test: Measuring memory usage
def memory_test(duration=5):
    logger.info(f"Starting Memory performance test for {duration} seconds...")
    start_time = time.time()
    memory_usage = psutil.virtual_memory().percent
    logger.info(f"Memory Usage: {memory_usage}% before test")
    
    # Simulating memory consumption
    memory_data = []
    while time.time() - start_time < duration:
        memory_data.append(np.random.rand(1000, 1000))  # Consuming memory
    
    memory_usage_after = psutil.virtual_memory().percent
    logger.info(f"Memory Usage: {memory_usage_after}% after test")
    return memory_usage, memory_usage_after

if __name__ == "__main__":
    # Run CPU, GPU, and memory tests
    cpu_usage = cpu_test()
    gpu_usage = gpu_test()
    memory_usage_before, memory_usage_after = memory_test()
    
    logger.info(f"Final CPU Usage: {cpu_usage}%")
    if gpu_usage is not None:
        logger.info(f"Final GPU Usage: {gpu_usage}%")
    logger.info(f"Memory Usage Before Test: {memory_usage_before}%")
    logger.info(f"Memory Usage After Test: {memory_usage_after}%")