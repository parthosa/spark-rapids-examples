
import json
import logging
import os
import sys
from datetime import datetime

# Modify sys.path to include the parent directory for local imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
print(sys.path)

from core.config import ConfigLoader
from core.notebook import NotebookOrchestrator
from databricks.cluster import DatabricksClusterManager
from databricks.runner import DatabricksNotebookRunner


def main(user_config_path: str) -> None:
            
    logging.basicConfig(
        level='INFO',
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    logger = logging.getLogger('NotebookAutomation')
    try:
        # Load configuration
        config = ConfigLoader.load_config(user_config_path)

        
        # Initialize managers
        orchestrator = NotebookOrchestrator(config, logger)
        cluster_manager = DatabricksClusterManager(config, logger)
        notebook_runner = DatabricksNotebookRunner(config, logger)
        
        # Import notebook from GitHub
        logger.info("Preparing notebook from GitHub...")
        workspace_path = orchestrator.prepare_notebook()
        
        # Create cluster
        logger.info("Creating cluster...")
        cluster_id = cluster_manager.create_cluster(
            cluster_name=f"GitHub_Notebook_Runner_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        )
        
        try:
            # Run notebook
            logger.info("Running notebook...")
            result = notebook_runner.run_notebook(
                cluster_id=cluster_id,
                notebook_path=workspace_path
            )
            
            logger.info("Run completed successfully!")
            logger.info(f"Run Output: {json.dumps(result['output'], indent=2)}")
            
        finally:
            logger.info("Terminating cluster...")
            cluster_manager.terminate_cluster(cluster_id)
            
    except Exception as e:
        logger.error(f"Error in notebook execution: {str(e)}", exc_info=True)
        raise

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python -m databricks_automation <config.json>")
        sys.exit(1)
    
    user_config_path = sys.argv[1]
    if not os.path.exists(user_config_path):
        print(f"Configuration file not found: {user_config_path}")
        sys.exit(1)
    
    if not user_config_path.endswith(".json"):
        print("Configuration file must be a JSON file")
        sys.exit(1)

    main(user_config_path)
