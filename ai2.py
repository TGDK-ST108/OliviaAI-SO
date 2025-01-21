import random
import time

class RealTimeAIModel(AIModel):
    def __init__(self):
        super().__init__()
        self.dynamic_priority_threshold = 2  # Threshold to adjust priority dynamically (can be tweaked based on system load)
    
    def dynamic_task_priority(self, tasks):
        """
        Adjust the priority of tasks dynamically based on system conditions (e.g., load or new incoming tasks).
        
        Arguments:
        - tasks: List of tasks to prioritize.
        
        Returns:
        - Sorted list of tasks based on dynamic priority.
        """
        adjusted_tasks = []
        for task, priority in tasks:
            # Simulate adjusting task priority based on dynamic conditions (e.g., system load)
            if random.random() > 0.5:  # Simulating real-time load or data fluctuation
                priority = "major"  # Boost task to major
            adjusted_tasks.append((task, priority))
        
        return self.prioritize_tasks(adjusted_tasks)
    
    def execute_task(self, task):
        """
        Override the execution to simulate real-time task handling.
        """
        task_data, priority = task
        print(f"Executing task: {task_data} with priority: {priority} - Real-time execution.")
        # Simulate real-time task execution
        time.sleep(random.uniform(0.5, 2))  # Simulating variable task execution time
    
    def run(self, tasks):
        """
        Run the tasks in real-time with dynamic prioritization and task handling.
        """
        sorted_tasks = self.dynamic_task_priority(tasks)
        for task in sorted_tasks:
            self.execute_task(task)

# Example usage of real-time AI model
real_time_ai_model = RealTimeAIModel()
tasks = [("task1", "upper"), ("task2", "lower"), ("task3", "upper"), ("task4", "lower")]

print("Starting real-time task execution:")
real_time_ai_model.run(tasks)