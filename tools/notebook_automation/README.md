# Notebook Automation

This module automates the execution of Qualification notebook on Databricks. The automation script will:
1. Copy the Qualification notebook to the Databricks workspace.
2. Create a new single-node cluster.
3. Run the Qualification notebook on the cluster.


## Configuration

To run the notebooks, you need to configure the `user_configs.json` file (e.g. databricks token, workspace URL, event log path, etc.).

## Running the Notebook Automation

Once the `user_configs.json` file is properly configured, you can run the automation script using the following command:

```bash
# Create a new single-node cluster based on the configuration in user_configs.json
python src/main.py user_configs.json create_cluster

# Run the notebook on the created cluster
python src/main.py user_configs.json run_notebook

# Delete the cluster after notebook execution is complete
python src/main.py user_configs.json delete_cluster 
```


### Why Split into Three Parts?

The automation is split into three separate commands to align with Jenkins pipeline stages:

1. `create_cluster` - Creates a fresh cluster environment
2. `run_notebook` - Executes the notebook on the created cluster  
3. `delete_cluster` - Handles cleanup of resources

There is an internal state manager that stores the cluster ID in a JSON file after cluster creation. The `run_notebook` and `delete_cluster` commands will read this stored cluster ID to execute their operations on the correct cluster.

### Additional Notes

To update user configs via the command line, you can use the `update_user_configs.sh` script. The script takes the path to the `user_configs.json` file as an argument. Example with supported environment variables:

```bash
# Configs for 'databricks' 
export WORKSPACE_URL="https://adb-2222222222222222.azuredatabricks.net"
export DATABRICKS_TOKEN="dapi22222222222222222222"

# Configs for 'github'
export REPO_URL="https://github.com/NVIDIA/spark-rapids-examples"
export BRANCH="main"
export NOTEBOOK_PATH="path/to/notebook.ipynb"

# Configs for 'workspace'
export IMPORT_PATH="/Workspace/new/path/to/user/home/"

# Configs for 'cluster'
export SPARK_VERSION="13.3.x-scala2.12"
export NODE_TYPE_ID="Standard_DS3_v2"

# Configs for 'notebook parameters'
export TOOLS_VERSION="24.12.0"
export EVENTLOG_PATH="dbfs:/new/path/to/eventlog"

./src/resources/update_user_configs.sh /path/to/user_configs.json
```