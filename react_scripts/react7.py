import requests
import os
from dotenv import load_dotenv

load_dotenv()
token = os.getenv("GITHUB_TOKEN")

if not token:
    raise ValueError("GitHub token not found. Please set GITHUB_TOKEN in your .env file.")

def compute_react7(full_name):
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "Authorization": f"token {token}"
    }

    repo_url = f'https://api.github.com/repos/{full_name}/contents/'

    linting_files = {
        ".pylintrc", ".clang-format", ".eslintrc.json", ".prettierrc", ".stylelintrc",
        ".editorconfig", "flake8", "pylintrc", "checkstyle.xml", ".rubocop.yml"
    }

    response = requests.get(repo_url, headers=headers)
    if response.status_code != 200:
        print(f"Error fetching contents for {full_name}, Status Code: {response.status_code}")
        return 0  

    repo_contents = response.json()
    if not isinstance(repo_contents, list):  
        return 0  

    found_files_count = sum(1 for file in repo_contents if file.get('name', '') in linting_files)

    return found_files_count if found_files_count > 0 else 0


