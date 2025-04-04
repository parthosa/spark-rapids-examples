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
from dataclasses import dataclass
from datetime import datetime
from typing import Any

import requests

from .databricks import DatabricksPlatform


@dataclass
class DatabricksNotebookRunner(DatabricksPlatform):
    """Manages Databricks notebook run operations"""

    def run_notebook(
        self, cluster_id: str, notebook_path: str = None, parameters: dict[str, Any] = None
    ) -> dict[str, Any]:
        notebook_path = notebook_path or self.config["notebook"]["path"]
        all_parameters = self.config["notebook"]["parameters"].copy()
        if parameters:
            all_parameters.update(parameters)

        notebook_task = {"notebook_path": notebook_path, "base_parameters": all_parameters}
        run_name = (
            f"{self.config['notebook']['run_prefix']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        )
        payload = {
            "run_name": run_name,
            "notebook_task": notebook_task,
            "existing_cluster_id": cluster_id,
        }

        self.logger.info(f"Submitting notebook run: {notebook_path}")
        response = requests.post(self.api.jobs["submit_run"], headers=self.headers, json=payload)
        if response.status_code != 200:
            raise Exception(f"Failed to submit notebook run: {response.text}")

        run_id = response.json()["run_id"]
        self.logger.info(f"Started run with ID: {run_id}")

        # Get run details including run_page_url
        run_response = requests.get(
            self.api.jobs["get_run"], headers=self.headers, params={"run_id": run_id}
        )
        if run_response.status_code != 200:
            raise Exception(f"Failed to get run details: {run_response.text}")

        run_page_url = run_response.json()["run_page_url"]
        self.logger.info(f"Monitor progress at: {run_page_url}")

        timeout_minutes = self.config["notebook"]["default_timeout_minutes"]
        check_interval = self.config["notebook"]["status_check_interval_seconds"]
        timeout = time.time() + (timeout_minutes * 60)

        while time.time() < timeout:
            status = self._get_run_status(run_id)

            if status["life_cycle_state"] == "TERMINATED":
                run_output = self._get_run_output(run_id)
                if status["result_state"] == "SUCCESS":
                    self.logger.info("Notebook run completed successfully")
                    return {"run_id": run_id, "status": "SUCCESS", "output": run_output}
                else:
                    error_trace = run_output.get("error_trace", "No error trace available")
                    if error_trace:
                        error_trace = error_trace.encode().decode("unicode-escape")
                    error_message = f"Notebook run failed with status: {status['result_state']}"
                    self.logger.error(error_message + f"\nError trace: {error_trace}")
                    raise Exception(error_message)

            self.logger.debug(f"Current state: {status['life_cycle_state']}")
            time.sleep(check_interval)

        raise TimeoutError(f"Notebook run timed out after {timeout_minutes} minutes")

    def _get_run_status(self, run_id: str) -> dict[str, Any]:
        response = requests.get(
            self.api.jobs["get_run"], headers=self.headers, params={"run_id": run_id}
        )
        if response.status_code != 200:
            raise Exception(f"Failed to get run status: {response.text}")
        return response.json()["state"]

    def _get_run_output(self, run_id: str) -> dict[str, Any]:
        response = requests.get(
            self.api.jobs["get_output"], headers=self.headers, params={"run_id": run_id}
        )
        if response.status_code != 200:
            raise Exception(f"Failed to get run output: {response.text}")
        return response.json()
