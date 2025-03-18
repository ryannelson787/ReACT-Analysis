import requests
import ollama
import os
from dotenv import load_dotenv

load_dotenv()
token = os.getenv("GITHUB_TOKEN")

if not token:
    raise ValueError("GitHub token not found. Please set GITHUB_TOKEN in your .env file.")

def compute_react67(full_name):
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "Authorization": f"token {token}"
    }

    issues_url = f'https://api.github.com/repos/{full_name}/issues?state=open&labels=needs%20help,bug'
    
    response = requests.get(issues_url, headers=headers)
    if response.status_code != 200:
        print(f"Error fetching issues for {full_name}, Status Code: {response.status_code}")
        return 0  

    issues = response.json()
    if not issues:
        return 0  

    issue_descriptions = [
        issue["title"] + "\n" + issue.get("body", "") 
        for issue in issues[:3]
    ]

    if not issue_descriptions:
        return 0  

    query = f"Analyze the following GitHub issue descriptions and determine if they clearly communicate the unresolved problem:\n\n{issue_descriptions}\n\nRespond with either a YES or a NO and nothing else!"
    
    ollama_response = ollama.chat(model="llama2:7b", messages=[{"role": "user", "content": query}])

    return 1 if ollama_response.get("message", {}).get("content", "").strip() == "YES" else 0

