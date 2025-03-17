import json
import requests
import re
from datetime import datetime, timedelta
from pydriller import Repository
from collections import defaultdict
import ollama
 
def react_26(full_name):

    token = "github_token"
    headers = {"Accept": "application/vnd.github.v3+json", "Authorization": f"token {token}"}
    
    repo_url = f"https://api.github.com/repos/{full_name}"

    test_files = ["tests/", "__tests__/", "test/", "spec/"]
    ci_files = [
        ".github/workflows/",
        ".travis.yml",
        "Jenkinsfile",
        ".circleci/config.yml",
        "azure-pipelines.yml",
        "bitbucket-pipelines.yml",
        "gitlab-ci.yml",
        "circle.yml"
    ]

    ci_badges = ["github.com/actions", "travis-ci.com", "circleci.com", "jenkins.io"]
    
    response = requests.get(f"{repo_url}/contents", headers=headers)
    repo_contents = response.json() if response.status_code == 200 else []

    test_files_found = any(test_file in [item["name"] for item in repo_contents] for test_file in test_files)

    response = requests.get(f"{repo_url}/contents/.github/workflows", headers=headers)
    if response.status_code == 200:
        ci_workflows = {item["name"]: requests.get(item["download_url"]).text for item in response.json()}
    else:
        ci_workflows = {}
    
    query = f"""Analyze the following GitHub repository for unit testing practices. Test files found: {'Yes' if test_files_found else 'No'}.
    CI/CD workflows: {ci_workflows if ci_workflows else 'No CI workflows detected'}. 
    Based on your analysis, just reply with a True if unit tests are actively conducted, otherwise return False. Here is the repository: {repo_url}. 
    Remember, only reply with True or False."""
    response = ollama.chat(model="llama3:8b", messages=[{"role": "user", "content": query}])

    return response['message']['content']

print(react_26("public-apis/public-apis")) 
