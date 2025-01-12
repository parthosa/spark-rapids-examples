import requests
from typing import Dict

class DatabricksAPIEndpoints:
    """Manages all Databricks API endpoints"""
    def __init__(self, domain: str):
        self.domain = domain.rstrip('/')
        
    @property
    def clusters(self) -> Dict[str, str]:
        return {
            'create': f"{self.domain}/api/2.0/clusters/create",
            'get': f"{self.domain}/api/2.0/clusters/get",
            'delete': f"{self.domain}/api/2.0/clusters/delete"
        }
    
    @property
    def jobs(self) -> Dict[str, str]:
        return {
            'submit_run': f"{self.domain}/api/2.0/jobs/runs/submit",
            'get_run': f"{self.domain}/api/2.0/jobs/runs/get",
            'get_output': f"{self.domain}/api/2.0/jobs/runs/get-output"
        }
    
    @property
    def workspace(self) -> Dict[str, str]:
        return {
            'import': f"{self.domain}/api/2.0/workspace/import",
            'get_status': f"{self.domain}/api/2.0/workspace/get-status",
            'delete': f"{self.domain}/api/2.0/workspace/delete"
        }
