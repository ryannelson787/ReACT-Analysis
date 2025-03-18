import requests
from datetime import datetime, timedelta
import ollama
import os
from dotenv import load_dotenv
    
def react_30(full_name):

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

    response = requests.get(f"{repo_url}/contents", headers=headers)
    if response.status_code == 200:
        repo_files = {
            file["name"]: file["download_url"]
            for file in response.json()
            if any(ci in file["name"] for ci in ci_files) and file.get("download_url")
        }
    else:
        repo_files = {}

    response = requests.get(f"{repo_url}/contents/.github/workflows", headers=headers)
    if response.status_code == 200:
        workflow_files = {
            file["name"]: file["download_url"]
            for file in response.json()
            if file.get("download_url") 
        }
    else:
        workflow_files = {}

    repo_files.update(workflow_files)

    configs = {}
    for name, url in repo_files.items():
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            configs[name] = response.text

    since_date = (datetime.now() - timedelta(days=30)).isoformat()
    params = {"since": since_date}
    response = requests.get(f"{repo_url}/commits", headers=headers, params=params)

    if response.status_code == 200:
        recent_commits = response.json()
    else:
        recent_commits = []
    
    ci_related_commits = 0
    total_commits = len(recent_commits)

    for commit in recent_commits:
        commit_message = commit["commit"]["message"].lower()
        if any(keyword in commit_message for keyword in ["ci", "build", "test", "workflow", "actions", "pipeline"]):
            ci_related_commits += 1

    commit_findings = {
        "total_commits": total_commits,
        "ci_related_commits": ci_related_commits,
        "ci_usage_ratio": round(ci_related_commits / total_commits, 2) if total_commits > 0 else 0
    }
    
    query = f"""Analyze the provided GitHub repository to determine if continuous integration (CI) is implemented.
    CI/CD Configuration Files Found: {list(configs.keys())}. Configuration Content: {configs}
    Recent CI/CD Activity in Commits:
    1. Total Commits Analyzed: {commit_findings["total_commits"]}
    2. Commits Related to CI/CD: {commit_findings["ci_related_commits"]}
    3. CI/CD Usage Ratio: {commit_findings["ci_usage_ratio"]}

    Based on your analysis, just reply with a True if this repository has 
    1. a working CI/CD pipeline.
    2. builds and automated tests are triggered on commits or pull requests.
    3. CI  is enforced before merging pull requests.
    otherwise return False. Here is the repository: {repo_url}. 
    Remember, only reply with True or False."""

    response = ollama.chat(model="llama3:8b", messages=[{"role": "user", "content": query}])

    return response['message']['content']

# print(react_30("public-apis/public-apis")) 
