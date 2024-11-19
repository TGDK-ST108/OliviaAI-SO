
import yaml

class ConfigManager:
    def __init__(self, config_file='config.yaml'):
        self.config = self.load_config(config_file)

    def load_config(self, config_file):
        with open(config_file, 'r') as f:
            config = yaml.safe_load(f)
        return config

    def get_database_config(self):
        return self.config.get('database', {})
