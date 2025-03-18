import requests
import os
from dotenv import load_dotenv

load_dotenv()
token = os.getenv("GITHUB_TOKEN")

if not token:
    raise ValueError("GitHub token not found. Please set GITHUB_TOKEN in your .env file.")

def compute_react3(full_name):
    repo_url = f'https://api.github.com/repos/{full_name}/languages'
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "Authorization": f"token {token}"
    }

    common_languages = {
        "Python", "Java", "JavaScript", "TypeScript", "C", "C++", "C#", 
        "Go", "Rust", "Swift", "Ruby", "Kotlin", "PHP", "R", "Perl"
    }

    response = requests.get(repo_url, headers=headers)

    if response.status_code != 200:
        print(f"Error fetching languages for {full_name}, Status Code: {response.status_code}")
        return 0  

    languages = response.json()

    return sum(1 for lang in languages.keys() if lang in common_languages)
