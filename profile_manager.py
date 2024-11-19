import logging

class ProfileManager:
    def __init__(self):
        self.profiles = {}
        self.data_store = {}  # Initialize a data store for storing data

    def create_profile(self, profile_id, task_type, data_source, priority_level, metadata=None):
        profile = DataProfile(profile_id, task_type, data_source, priority_level, metadata)
        self.profiles[profile_id] = profile

    def get_profile(self, profile_id):
        """Retrieves profile by ID."""
        return self.profiles.get(profile_id, None)

    def update_profile_metadata(self, profile_id, key, value):
        profile = self.get_profile(profile_id)
        if profile:
            profile.add_metadata(key, value)

    def store_data(self, data, data_label):
        """
        Stores the given data with the specified label.
        """
        self.data_store[data_label] = data
        logging.info(f"Data stored with label '{data_label}'")
