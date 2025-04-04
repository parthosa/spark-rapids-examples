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

import argparse
import base64
import os
import sys
from datetime import datetime

import nbformat
from github import Github


def update_notebook_variable(repo_name, notebook_path, variable_name, new_value, branch_name=None):
    """
    Updates a variable in a Jupyter notebook and creates a PR.

    Args:
        repo_name (str): Format 'owner/repository'
        notebook_path (str): Path to notebook in repository
        variable_name (str): Name of variable to update
        new_value (any): New value for the variable
        branch_name (str, optional): Name for new branch. Defaults to auto-generated name.
    """
    try:
        # Initialize GitHub client
        github_token = os.environ.get("GITHUB_TOKEN")
        if not github_token:
            raise ValueError("Please set GITHUB_TOKEN environment variable")

        g = Github(github_token)
        repo = g.get_repo(repo_name)

        # Get the main branch
        default_branch = repo.default_branch
        main_ref = repo.get_git_ref(f"heads/{default_branch}")

        # Create new branch if not specified
        if branch_name is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            branch_name = f"update_variable_{timestamp}"

        # Create new branch
        repo.create_git_ref(ref=f"refs/heads/{branch_name}", sha=main_ref.object.sha)

        # Get notebook content
        notebook_content = repo.get_contents(notebook_path, ref=branch_name)
        notebook_data = base64.b64decode(notebook_content.content)
        notebook = nbformat.reads(notebook_data.decode("utf-8"), as_version=4)

        # Find and update the variable
        variable_found = False
        for cell in notebook.cells:
            if cell.cell_type == "code":
                if variable_name in cell.source:
                    # Simple replacement - you might want to make this more robust
                    lines = cell.source.split("\n")
                    for i, line in enumerate(lines):
                        if line.strip().startswith(variable_name + " ="):
                            lines[i] = f"{variable_name} = {repr(new_value)}"
                            variable_found = True
                            break
                    if variable_found:
                        cell.source = "\n".join(lines)
                        break

        if not variable_found:
            raise ValueError(f"Variable {variable_name} not found in notebook")

        # Convert notebook back to string
        updated_content = nbformat.writes(notebook)

        # Create commit
        repo.update_file(
            notebook_path,
            f"Update {variable_name} in {notebook_path}",
            updated_content,
            notebook_content.sha,
            branch=branch_name,
        )

        # Create pull request
        pr = repo.create_pull(
            title=f"Update {variable_name} in {notebook_path}",
            body=f"Automated update of {variable_name} to {new_value}",
            head=branch_name,
            base=default_branch,
        )

        return pr.html_url
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="Update a variable in a Jupyter notebook and create a PR"
    )
    parser.add_argument(
        "--repo", required=True, help="GitHub repository in format owner/repository"
    )
    parser.add_argument("--notebook", required=True, help="Path to the notebook in the repository")
    parser.add_argument("--variable", required=True, help="Name of the variable to update")
    parser.add_argument("--value", required=True, help="New value for the variable")
    parser.add_argument("--branch", help="Name for the new branch (optional)")

    args = parser.parse_args()

    try:
        pr_url = update_notebook_variable(
            repo_name=args.repo,
            notebook_path=args.notebook,
            variable_name=args.variable,
            new_value=args.value,
            branch_name=args.branch,
        )
        print(f"Successfully created PR: {pr_url}")
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
