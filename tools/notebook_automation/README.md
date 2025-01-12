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
python src/main.py /path/to/user_configs.json
```

