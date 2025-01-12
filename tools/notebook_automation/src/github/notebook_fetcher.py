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
