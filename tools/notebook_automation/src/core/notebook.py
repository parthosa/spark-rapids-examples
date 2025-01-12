import os
import logging
from typing import Dict, Any

from github.notebook_fetcher import GitHubNotebookFetcher
from databricks.workspace import DatabricksWorkspaceManager


class NotebookOrchestrator:
    """Orchestrates the notebook import and execution process"""
    def __init__(self, config: Dict[str, Any], logger: logging.Logger):
        self.config = config
        self.logger = logger
        self.workspace_manager = DatabricksWorkspaceManager(config, logger)
        
    def prepare_notebook(self) -> str:
        """Fetch notebook from GitHub and import to Databricks"""
        github_config = self.config['github']
        
        self.logger.info(f"Fetching notebook from GitHub: {github_config['notebook_path']}")
        content = GitHubNotebookFetcher.fetch_notebook_content(
            github_config['repo_url'],
            github_config['notebook_path'],
            github_config['branch']
        )
        
        notebook_name = os.path.basename(github_config['notebook_path'])
        workspace_path = os.path.join(
            self.config['workspace']['import_path'],
            notebook_name
        )
        
        return self.workspace_manager.import_notebook(content, workspace_path)
