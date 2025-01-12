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

import time
import requests
from dataclasses import dataclass

from .databricks import DatabricksPlatform

@dataclass
class DatabricksClusterManager(DatabricksPlatform):
    """ Manages Databricks cluster operations """
    
    def create_cluster(self, cluster_name: str) -> str:
        cluster_config = self.config['cluster']['default_config'].copy()
        cluster_config['cluster_name'] = cluster_name
        
        self.logger.info(f"Creating cluster: {cluster_name}")
        response = requests.post(self.api.clusters['create'], 
                               headers=self.headers, 
                               json=cluster_config)
        if response.status_code != 200:
            raise Exception(f"Failed to create cluster: {response.text}")
            
        cluster_id = response.json()['cluster_id']
        self.logger.info(f"Created cluster with ID: {cluster_id}")
        
        timeout_minutes = self.config['cluster']['creation_timeout_minutes']
        timeout = time.time() + (timeout_minutes * 60)
        while time.time() < timeout:
            status = self._get_cluster_state(cluster_id)
            self.logger.debug(f"Cluster state: {status}")
            
            if status == "RUNNING":
                return cluster_id
            elif status in ["ERROR", "TERMINATED", "UNKNOWN"]:
                raise Exception(f"Cluster failed to start. Final state: {status}")
                
            time.sleep(30)
            
        raise TimeoutError(f"Cluster creation timed out after {timeout_minutes} minutes")
    
    def _get_cluster_state(self, cluster_id: str) -> str:
        response = requests.get(self.api.clusters['get'], 
                              headers=self.headers, 
                              params={"cluster_id": cluster_id})
        if response.status_code != 200:
            raise Exception(f"Failed to get cluster state: {response.text}")
        return response.json()['state']
    
    def terminate_cluster(self, cluster_id: str) -> None:
        self.logger.info(f"Terminating cluster: {cluster_id}")
        response = requests.post(self.api.clusters['delete'], 
                               headers=self.headers, 
                               json={"cluster_id": cluster_id})
        if response.status_code != 200:
            raise Exception(f"Failed to terminate cluster: {response.text}")
        self.logger.info(f"Terminated cluster: {cluster_id}")
