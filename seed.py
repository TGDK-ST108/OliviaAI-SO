
import yaml
import logging
from typing import Any

class IntroducedSeed:
    def __init__(self, config_path: str = "config.yaml"):
        self.config = self.load_config(config_path)
        logging.info("IntroducedSeed initialized with config: %s", config_path)

    def load_config(self, path: str) -> dict:
        with open(path, 'r') as file:
            config = yaml.safe_load(file)
        return config

    def get_seed_parameter(self, parameter: str) -> Any:
        value = self.config.get(parameter)
        logging.info("Retrieved seed parameter '%s': %s", parameter, value)
        return value
