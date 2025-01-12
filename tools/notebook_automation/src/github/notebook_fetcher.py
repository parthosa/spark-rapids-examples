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

import requests
from urllib.parse import urlparse, quote

class GitHubNotebookFetcher:
    """Handles fetching notebooks from GitHub"""
    
    @staticmethod
    def get_raw_notebook_url(repo_url: str, notebook_path: str, branch: str = "main") -> str:
        """Convert GitHub URL to raw content URL"""
        parsed = urlparse(repo_url)
        path_parts = parsed.path.strip('/').split('/')
        raw_url = f"https://raw.githubusercontent.com/{path_parts[0]}/{path_parts[1]}/{branch}/{notebook_path}"
        return quote(raw_url, safe=":/[]")
    
    @staticmethod
    def fetch_notebook_content(repo_url: str, notebook_path: str, branch: str = "main") -> str:
        """Fetch notebook content from GitHub"""
        raw_url = GitHubNotebookFetcher.get_raw_notebook_url(repo_url, notebook_path, branch)
        response = requests.get(raw_url)
        if response.status_code != 200:
            raise Exception(f"Failed to fetch notebook from GitHub: {response.text}")
        return response.content
