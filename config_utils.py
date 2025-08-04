"""
Shared configuration utility for reading settings from JSON files.
"""
import json
import os


def load_config():
    """
    Load configuration from JSON file.
    
    Returns:
        dict: Configuration dictionary
        
    Raises:
        FileNotFoundError: If the configuration file is not found
        ValueError: If the JSON file is invalid
    """
    config_file = 'config.json'
    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            config = json.load(f)
        return config
    except FileNotFoundError:
        raise FileNotFoundError(f"Configuration file '{config_file}' not found. Please create it with the required settings.")
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON in configuration file '{config_file}': {e}")


def get_config_value(config, key):
    """
    Get a value from the configuration dictionary.
    
    Args:
        config (dict): Configuration dictionary
        key (str): Key to retrieve
        
    Returns:
        The configuration value
        
    Raises:
        KeyError: If key is missing
    """
    if key not in config:
        raise KeyError(f"Configuration key '{key}' is missing from config file")
    return config[key]
