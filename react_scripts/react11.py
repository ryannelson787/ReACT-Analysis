import requests
import os
from dotenv import load_dotenv

load_dotenv()
token = os.getenv("GITHUB_TOKEN")

if not token:
    raise ValueError("GitHub token not found. Please set GITHUB_TOKEN in your .env file.")


def compute_react11(full_name):
    repo_url = f'https://api.github.com/repos/{full_name}'
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "Authorization": f"token {token}"
    }

    response = requests.get(repo_url, headers=headers)

    if response.status_code != 200:
        print(f"Error fetching {full_name}, Status Code: {response.status_code}")
        return 0  

    repo_data = response.json()
    repo_size = repo_data.get("size", float('inf'))

    print(f"Repo: {full_name}, Size: {repo_size}")
   
    return 1 if repo_size < 500000 else 0


