# config_validation.py

import logging

def validate_config(config):
    """
    Validate the configuration dictionary to ensure all required fields are present.
    """
    required_fields = ['compliance_standards', 'siem', 'key_vault', 'network_ranges']
    for field in required_fields:
        if field not in config:
            logging.error(f"Missing required configuration field: {field}")
            raise ValueError(f"Missing required configuration field: {field}")

    # Validate SIEM configuration
    siem_required_fields = ['type', 'host', 'port', 'username', 'password']
    if 'siem' in config:
        for field in siem_required_fields:
            if field not in config['siem']:
                logging.error(f"Missing '{field}' in SIEM configuration.")
                raise ValueError(f"Missing '{field}' in SIEM configuration.")

    # Validate key_vault configuration
    key_vault_required_fields = ['uri', 'secret_name']
    if 'key_vault' in config:
        for field in key_vault_required_fields:
            if field not in config['key_vault']:
                logging.error(f"Missing '{field}' in key_vault configuration.")
                raise ValueError(f"Missing '{field}' in key_vault configuration.")

    # Validate network_ranges
    if not isinstance(config.get('network_ranges'), list):
        logging.error("network_ranges must be a list.")
        raise ValueError("network_ranges must be a list.")

    logging.info("Configuration validation passed.")
