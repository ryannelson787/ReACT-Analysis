import json
import requests
import ollama
import os
from dotenv import load_dotenv
 
def react_26(full_name):

    load_dotenv()
    token = os.getenv("GITHUB_TOKEN")
    headers = {"Accept": "application/vnd.github.v3+json", "Authorization": f"token {token}"}
    
    repo_url = f"https://api.github.com/repos/{full_name}"

    test_files = ["tests/", "__tests__/", "test/", "spec/"]

    response = requests.get(f"{repo_url}/contents", headers=headers)
    repo_contents = response.json() if response.status_code == 200 else []

    test_files_found = any(item["name"] in test_files or any(ext in item["name"] for ext in [".test.", ".spec."]) for item in repo_contents)

    response = requests.get(f"{repo_url}/contents/.github/workflows", headers=headers)
    if response.status_code == 200:
        ci_workflows = {
            item["name"]: requests.get(item["download_url"]).text 
            for item in response.json() 
            if item.get("download_url")  
        }
    else:
        ci_workflows = {}
    
    query = f"""Analyze the following GitHub repository for unit testing practices. Test files found: {'Yes' if test_files_found else 'No'}.
    CI/CD workflows: {ci_workflows if ci_workflows else 'No CI workflows detected'}. 
    Based on your analysis, just reply with a True if unit tests are actively conducted, otherwise return False. Here is the repository: {repo_url}. 
    Remember, only reply with True or False."""
    response = ollama.chat(model="llama3:8b", messages=[{"role": "user", "content": query}])

    return response['message']['content']


# print(react_26("public-apis/public-apis")) 

