import base64
import logging
import os
import requests
from typing import Dict, Any
from .api import DatabricksAPIEndpoints

class DatabricksWorkspaceManager:
    """Manages Databricks workspace operations"""
    def __init__(self, config: Dict[str, Any], logger: logging.Logger):
        self.config = config
        self.logger = logger
        self.api = DatabricksAPIEndpoints(config['databricks']['domain'])
        self.headers = {
            'Authorization': f"Bearer {config['databricks']['token']}",
            'Content-Type': 'application/json'
        }
    
    def import_notebook(self, content: bytes, workspace_path: str) -> str:
        """Import notebook content into Databricks workspace"""
        import_payload = {
            "content": base64.b64encode(content).decode('utf-8'),
            "path": workspace_path,
            "format": "JUPYTER",
            "overwrite": self.config['workspace']['overwrite']
        }
        
        self.logger.info(f"Importing notebook to {workspace_path}")
        response = requests.post(
            self.api.workspace['import'],
            headers=self.headers,
            json=import_payload
        )
        
        if response.status_code != 200:
            raise Exception(f"Failed to import notebook: {response.text}")
            
        return workspace_path
