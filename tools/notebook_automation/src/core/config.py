# Copyright (c) 2025, NVIDIA CORPORATION.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
from typing import Any

import yaml


class ConfigLoader:
    app_configs_path: str = os.path.join("src", "resources", "app_configs.yaml")
    csp_configs_path: str = os.path.join("src", "resources", "csp_configs.yaml")

    @staticmethod
    def load_config_internal(config_path: str) -> dict[str, Any]:
        """Load configuration from YAML file"""
        if not os.path.exists(config_path):
            raise FileNotFoundError(f"Configuration file not found: {config_path}")

        with open(config_path) as f:
            config = yaml.safe_load(f)
        return config

    @classmethod
    def load_csp_config(cls, app_configs, platform: str) -> dict[str, Any]:
        """Load CSP configuration"""
        csp_configs = ConfigLoader.load_config_internal(cls.csp_configs_path)
        app_configs["cluster"]["csp_configs"] = csp_configs[platform]

    @classmethod
    def load_config(cls, user_config_path: str, platform: str) -> dict[str, Any]:
        """Load configuration from YAML file"""
        app_configs = ConfigLoader.load_config_internal(cls.app_configs_path)
        cls.load_csp_config(app_configs, platform)
        user_config = cls.load_config_internal(user_config_path)
        cls.update_config(app_configs, user_config)
        app_configs["cluster"]["default_config"]["driver_node_type_id"] = app_configs["cluster"][
            "default_config"
        ]["node_type_id"]
        return app_configs

    @classmethod
    def update_config(cls, config: dict[str, Any], new_config: dict[str, Any]):
        """Update configuration with new values"""
        for key, value in new_config.items():
            if isinstance(value, dict) and key in config and isinstance(config[key], dict):
                cls.update_config(config[key], value)
            else:
                config[key] = value
