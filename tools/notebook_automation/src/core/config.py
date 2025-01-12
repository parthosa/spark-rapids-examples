
import json
import os
from typing import Dict, Any

class ConfigLoader:
    app_configs_path: str = os.path.join('src', 'resources', 'app_configs.json')
    csp_configs_path: str = os.path.join('src', 'resources', 'csp_configs.json')

    @staticmethod
    def load_config_internal(config_path: str) -> Dict[str, Any]:
        """Load configuration from JSON file"""
        if not os.path.exists(config_path):
            raise FileNotFoundError(f"Configuration file not found: {config_path}")
            
        with open(config_path, 'r') as f:
            config = json.load(f)
        return config
    
    @classmethod
    def load_csp_config(cls, app_configs) -> Dict[str, Any]:
        """Load CSP configuration"""
        csp_configs = ConfigLoader.load_config_internal(cls.csp_configs_path)
        for key in csp_configs:
            if key in app_configs:
                app_configs['cluster']['default_config'][key] = csp_configs[key]

    
    @classmethod
    def load_config(cls, user_config_path: str) -> Dict[str, Any]:
        """Load configuration from JSON file"""
        app_configs = ConfigLoader.load_config_internal(cls.app_configs_path)
        cls.load_csp_config(app_configs)
        user_config = cls.load_config_internal(user_config_path)
        cls.update_config(app_configs, user_config)
        return app_configs

    @classmethod
    def update_config(cls, config: Dict[str, Any], new_config: Dict[str, Any]):
        """Update configuration with new values"""
        for key, value in new_config.items():
            if isinstance(value, dict) and key in config and isinstance(config[key], dict):
                cls.update_config(config[key], value)
            else:
                config[key] = value
        