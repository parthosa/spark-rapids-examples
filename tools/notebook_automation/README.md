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
./run.sh /path/to/user_configs.json
```


### Additional Notes

To update user configs via the command line, you can use the `update_user_configs.sh` script. The script takes the path to the `user_configs.json` file as an argument. Example with supported environment variables:

```bash
export WORKSPACE_URL="https://adb-2222222222222222.azuredatabricks.net"
export DATABRICKS_TOKEN="dapi22222222222222222222"
export IMPORT_PATH="/Workspace/new/path/to/user/home/"
export SPARK_VERSION="13.3.x-scala2.12"
export NODE_TYPE_ID="Standard_DS3_v2"
export TOOLS_VERSION="24.12.0"
export EVENTLOG_PATH="dbfs:/new/path/to/eventlog"

./src/resources/update_user_configs.sh /path/to/user_configs.json
```