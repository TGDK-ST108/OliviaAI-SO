class Figure8MemoryAllocator:
    def __init__(self, flow_type="parallel"):
        """
        Initialize the Figure8MemoryAllocator with the specified flow type.

        :param flow_type: Type of memory flow. Options: 'parallel', 'sequential'.
        """
        self.flow_type = flow_type

    def allocate(self, tasks):
        """
        Allocate tasks using the figure-8 memory flow.

        :param tasks: List of tasks to allocate.
        :return: Allocated tasks with figure-8 memory logic applied.
        """
        allocated_tasks = []
        memory_pool = []

        for idx, task in enumerate(tasks):
            if self.flow_type == "parallel":
                memory_pool.append(task)
                if idx % 2 == 0:  # Simulate figure-8 flow by alternating direction
                    memory_pool.reverse()
            elif self.flow_type == "sequential":
                allocated_tasks.append(task)
            else:
                raise ValueError("Invalid flow type. Use 'parallel' or 'sequential'.")

        if self.flow_type == "parallel":
            allocated_tasks.extend(memory_pool)

        print(f"Figure-8 memory flow allocated {len(allocated_tasks)} tasks.")
        return allocated_tasks