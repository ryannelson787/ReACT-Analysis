import requests
import ollama
import os
from dotenv import load_dotenv
import time

def get_all_files(repo_url, headers, path=""):
    url = f"{repo_url}/contents/{path}" if path else f"{repo_url}/contents"
    response = requests.get(url, headers=headers)
    time.sleep(1)  # Prevent API rate-limiting

    if response.status_code == 200:
        contents = response.json()
        files = []
        for item in contents:
            if item["type"] == "file" and item.get("download_url"):
                files.append(item["path"])
            elif item["type"] == "dir":
                files.extend(get_all_files(repo_url, headers, item["path"]))
        return files
    return []
 
def react_66(full_name):

    load_dotenv()
    token = os.getenv("GITHUB_TOKEN")
    headers = {"Accept": "application/vnd.github.v3+json", "Authorization": f"token {token}"}
    
    repo_url = f"https://api.github.com/repos/{full_name}"
    default_branch = "main"

    test_patterns = ["tests/", "__tests__/", "test/", "spec/", ".test.", ".spec."]
    ci_patterns = [
        ".github/workflows/", ".travis.yml", "Jenkinsfile", ".circleci/config.yml",
        "azure-pipelines.yml", "bitbucket-pipelines.yml", "gitlab-ci.yml", "circle.yml"
    ]
    coverage_patterns = [
        "coverage.xml", ".coveragerc", ".nycrc", "coverage/", "jest.config.js",
        "karma.conf.js", "jacoco.exec", "jacoco.xml", "cobertura.xml", ".csproj",
        "opencover.xml", "codecov.yml", ".coveralls.yml"
    ]
    
    repo_files = get_all_files(repo_url, headers)
    
    test_files_found = any(any(pattern in file for pattern in test_patterns) for file in repo_files)
    
    ci_workflows_found = any(any(pattern in file for pattern in ci_patterns) for file in repo_files)

    response = requests.get(f"{repo_url}/actions/runs", headers=headers)
    
    if response.status_code == 200:
        runs = response.json().get("workflow_runs", [])
        recent_success = any(run["conclusion"] == "success" for run in runs[:5])
    else:
        recent_success = False

    response = requests.get(f"{repo_url}/branches/{default_branch}/protection", headers=headers)
    
    if response.status_code == 200:
        rules = response.json()
        required_checks = rules.get("required_status_checks", {}).get("contexts", [])
        branch_protection = any("test" in check.lower() or "ci" in check.lower() for check in required_checks)
    else:
        branch_protection = False
    
    query = f"""Analyze the following GitHub repository for testing best practices.
    Test files found: {'Yes' if test_files_found else 'No'}.
    CI/CD workflows present: {'Yes' if ci_workflows_found else 'No'}.
    Recent Successful CI Runs: {'Yes' if recent_success else 'No'}.
    Branch Protection Requires Tests Before Merge: {'Yes' if branch_protection else 'No'}.

    Based on your analysis, just reply with True if the repo ensures proper testing before merging features, otherwise return False.
    Repository: {repo_url}.
    Remember, only reply with True or False."""

    response = ollama.chat(model="llama3:8b", messages=[{"role": "user", "content": query}])

    print(response["message"]['content']) 
    return response['message']['content']

# print(react_66("public-apis/public-apis")) 
