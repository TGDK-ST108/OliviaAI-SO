import ray

class DistributedTaskManager:
    def __init__(self, num_cpus=2):
        """
        Initialize the DistributedTaskManager with a specified number of CPUs.

        :param num_cpus: Number of CPUs to allocate for distributed processing.
        """
        self.num_cpus = num_cpus
        ray.init(num_cpus=self.num_cpus)

    @ray.remote
    def process_task(task):
        """
        Simulate the processing of a single task in a distributed manner.

        :param task: The task to process.
        :return: The processed result.
        """
        print(f"Processing Task ID: {task['task_id']}")
        return {"task_id": task["task_id"], "result": f"Processed {task['data']}"}

    def distribute_tasks(self, tasks):
        """
        Distribute tasks across available CPUs for parallel processing.

        :param tasks: List of tasks to distribute.
        :return: Results from all distributed tasks.
        """
        distributed_results = ray.get([self.process_task.remote(task) for task in tasks])
        print(f"Distributed {len(tasks)} tasks across {self.num_cpus} CPUs.")
        return distributed_results

    def shutdown(self):
        """
        Shut down the Ray cluster.
        """
        ray.shutdown()
        print("Ray cluster shut down.")