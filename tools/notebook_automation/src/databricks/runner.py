import time
import json
import requests
import logging
from datetime import datetime
from typing import Dict, Any
from .api import DatabricksAPIEndpoints
from core.utils import Utils

class DatabricksNotebookRunner:
    def __init__(self, config: Dict[str, Any], logger: logging.Logger):
        self.config = config
        self.logger = logger
        self.api = DatabricksAPIEndpoints(config['databricks']['domain'])
        self.headers = {
            'Authorization': f"Bearer {config['databricks']['token']}",
            'Content-Type': 'application/json'
        }

    def run_notebook(self, cluster_id: str, notebook_path: str = None, 
                    parameters: Dict[str, Any] = None) -> Dict[str, Any]:
        notebook_path = notebook_path or self.config['notebook']['path']
        all_parameters = self.config['notebook']['parameters'].copy()
        if parameters:
            all_parameters.update(parameters)
            
        notebook_task = {
            "notebook_path": notebook_path,
            "base_parameters": all_parameters
        }
            
        payload = {
            "run_name": f"API_Run_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "notebook_task": notebook_task,
            "existing_cluster_id": cluster_id
        }
        
        self.logger.info(f"Submitting notebook run: {notebook_path}")
        response = requests.post(self.api.jobs['submit_run'], 
                               headers=self.headers, 
                               json=payload)
        if response.status_code != 200:
            raise Exception(f"Failed to submit notebook run: {response.text}")
            
        run_id = response.json()['run_id']
        self.logger.info(f"Started run with ID: {run_id}")
        
        timeout_minutes = self.config['notebook']['default_timeout_minutes']
        check_interval = self.config['notebook']['status_check_interval_seconds']
        timeout = time.time() + (timeout_minutes * 60)
        
        while time.time() < timeout:
            status = self._get_run_status(run_id)
            
            if status['life_cycle_state'] == 'TERMINATED':
                run_output = self._get_run_output(run_id)
                if status['result_state'] == 'SUCCESS':
                    self.logger.info("Notebook run completed successfully")
                    return {
                        'run_id': run_id,
                        'status': 'SUCCESS',
                        'output': run_output
                    }
                else:
                    if 'error_trace' in run_output:
                        error_trace = run_output['error_trace'].encode().decode('unicode-escape')
                    error_message = f"Notebook run failed with status: {status['result_state']}"
                    self.logger.error(error_message + f"\nError trace: {error_trace}")
                    raise Exception(error_message)
            
            self.logger.debug(f"Current state: {status['life_cycle_state']}")
            time.sleep(check_interval)
            
        raise TimeoutError(f"Notebook run timed out after {timeout_minutes} minutes")
    
    def _get_run_status(self, run_id: str) -> Dict[str, Any]:
        response = requests.get(self.api.jobs['get_run'], 
                              headers=self.headers, 
                              params={"run_id": run_id})
        if response.status_code != 200:
            raise Exception(f"Failed to get run status: {response.text}")
        return response.json()['state']
    
    def _get_run_output(self, run_id: str) -> Dict[str, Any]:
        response = requests.get(self.api.jobs['get_output'], 
                              headers=self.headers, 
                              params={"run_id": run_id})
        if response.status_code != 200:
            raise Exception(f"Failed to get run output: {response.text}")
        return response.json()
