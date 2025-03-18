import requests
import os
from dotenv import load_dotenv

load_dotenv()
token = os.getenv("GITHUB_TOKEN")

if not token:
    raise ValueError("GitHub token not found. Please set GITHUB_TOKEN in your .env file.")

def compute_react23(full_name):
    issues_url = f'https://api.github.com/repos/{full_name}/issues?state=open'
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "Authorization": f"token {token}"
    }

    response = requests.get(issues_url, headers=headers)

    if response.status_code != 200:
        print(f"Error fetching issues for {full_name}, Status Code: {response.status_code}")
        return 0 

    issues = response.json()
    complexity_labels = {"beginner-friendly", "easy", "complex", "hard"}

    has_complexity_tag = any(
        "labels" in issue and any(label["name"].lower() in complexity_labels for label in issue["labels"])
        for issue in issues
    )

    #print(f"Repo: {full_name}, Has Complexity Tags: {has_complexity_tag}")
    
    return 1 if has_complexity_tag else 0


