import json
import requests
import re
from datetime import datetime, timedelta
from collections import defaultdict
import ollama
    
def react_6(full_name):

    token = "github_token"
    headers = {"Accept": "application/vnd.github.v3+json", "Authorization": f"token {token}"}
    
    repo_url = f"https://api.github.com/repos/{full_name}"

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
    if response.status_code == 200:
        files = [item["name"] for item in response.json()]
        has_ci_files = any(ci_file in files for ci_file in ci_files)
    else:
        has_ci_files = False

    response = requests.get(f"{repo_url}/readme", headers=headers)
    if response.status_code == 200:
        readme_content = requests.get(response.json()["download_url"]).text
        has_ci_badges = any(badge in readme_content for badge in ci_badges)
    else:
        has_ci_badges = False

    response = requests.get(f"{repo_url}/actions/runs", headers=headers)
    if response.status_code == 200:
        runs = response.json().get("workflow_runs", [])
        if not runs:
            has_recent_successful_runs = False
        has_recent_successful_runs = any(run["conclusion"] == "success" for run in runs[:5])
    else:
        has_recent_successful_runs = False
    
    print(f"CI Configuration Files Found: {has_ci_files}")
    print(f"CI/CD Badges in README: {has_ci_badges}")
    print(f"Recent Successful CI Runs: {has_recent_successful_runs}")
    
    # if has_ci_files or has_ci_badges or has_recent_successful_runs:
    #     return True
    # else:
    #     return False
    
    query = f"""Analyze the following GitHub repository for Continuous Integration (CI) maintenance. 
    Look for CI/CD configurations in {ci_files} and look for the following CI/CD badges {ci_badges} in the readme. 
    Identify whether automated tests are being executed, whether builds are passing, and if workflows are frequently run.
    Check for CI best practices such as linting, security scans, and deployment pipelines. 
    Based on your analysis, just reply with a True if this repository maintains CI, otherwise return False. Here is the repository: {repo_url}. 
    Remember, only reply with True or False."""

    response = ollama.chat(model="llama3:8b", messages=[{"role": "user", "content": query}])

    return response['message']['content']

print(react_6("public-apis/public-apis")) 
