class AIModel:
    def __init__(self):
        # Initialize AI model with basic priority rules
        self.priority_rules = {'major': 3, 'upper': 2, 'lower': 1}
    
    def prioritize_tasks(self, tasks):
        """
        Sort and prioritize tasks based on their willpower category (major, upper, lower).
        
        Arguments:
        - tasks: List of tuples, where each tuple contains task data and its priority level
                 Example: [("task1", "major"), ("task2", "upper"), ("task3", "lower")]
        
        Returns:
        - Sorted list of tasks based on priority
        """
        # Sort tasks by priority (major > upper > lower)
        sorted_tasks = sorted(tasks, key=lambda x: self.priority_rules[x[1]], reverse=True)
        return sorted_tasks
    
    def execute_task(self, task):
        """
        Execute the task based on its priority. Major tasks are executed first, followed by upper and lower.
        
        Arguments:
        - task: A tuple containing the task data and its priority level.
        """
        task_data, priority = task
        print(f"Executing task: {task_data} with priority: {priority}")
        # Simulate task execution logic (e.g., computation, data handling)
    
    def run(self, tasks):
        """
        Execute tasks in order of priority, handling major tasks first.
        
        Arguments:
        - tasks: List of tuples with tasks and their priority levels
        """
        sorted_tasks = self.prioritize_tasks(tasks)
        for task in sorted_tasks:
            self.execute_task(task)

# Example usage
ai_model = AIModel()
tasks = [("task1", "major"), ("task2", "upper"), ("task3", "lower"), ("task4", "major")]
ai_model.run(tasks)