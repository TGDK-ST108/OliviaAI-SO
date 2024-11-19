class DataProfile:
    def __init__(self, profile_id, task_type, data_source, priority_level, metadata=None):
        self.profile_id = profile_id  # Unique identifier
        self.task_type = task_type    # Type of task (e.g., prediction, pattern recognition)
        self.data_source = data_source  # Origin of the data
        self.priority_level = priority_level  # Priority for processing
        self.metadata = metadata if metadata else {}  # Additional profile information

    def add_metadata(self, key, value):
        """Adds or updates metadata for the profile."""
        self.metadata[key] = value

    def get_metadata(self, key):
        """Retrieves specific metadata value."""
        return self.metadata.get(key, None)
