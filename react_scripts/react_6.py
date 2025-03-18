import json
import requests
import re
from datetime import datetime, timedelta
from collections import defaultdict
import ollama
import os
from dotenv import load_dotenv
    
def react_6(full_name):

    load_dotenv()
    token = os.getenv("GITHUB_TOKEN")
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
    
    # print(f"CI Configuration Files Found: {has_ci_files}")
    # print(f"CI/CD Badges in README: {has_ci_badges}")
    # print(f"Recent Successful CI Runs: {has_recent_successful_runs}")
    
    if has_ci_files or has_ci_badges or has_recent_successful_runs:
        return True
    else:
        return False

# print(react_6("public-apis/public-apis")) 
