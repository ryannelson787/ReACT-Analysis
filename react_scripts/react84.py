import requests
import base64
import ollama
import git
import os
import random
from urllib.parse import urlparse
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()
github_token = os.getenv("GITHUB_TOKEN")

'''
ReACT_84: Provide onboarding support and help newcomers to make their first contribution


'''
def compute_react84(full_name):
    repo_url = f'https://github.com/{full_name}'

    parsed_url = urlparse(repo_url)
    owner = parsed_url.path.split('/')[1]
    repo_name = parsed_url.path.split('/')[2]

    local_url_base = f'repo_folder'
    local_url = f'repo_folder/{repo_name}'

    if not os.path.exists(local_url):
        os.system(f"git clone {repo_url} {local_url}")

    repo = git.Repo(local_url)
    repo.git.checkout(repo.head.commit)


    required_files = {
        "readme.md", "contributing.md", "code_of_conduct.md", "maintainers.md", "roadmap.md"
    }
    
    repo_files = {file: file.lower() for file in os.listdir(local_url)}
    found_files = {original for original, lower in repo_files.items() if lower in required_files}

    best_score = 0

    for file in found_files:
        with open(local_url + '/' + file, 'r', encoding="utf-8") as file:
            file_contents = file.read()

        query = f"Here is an md file:\n\n{file_contents}\n\nEND OF FILE\n\nThe file you just read is a file in a GitHub project. You are needed in order to determine, given this file, how easy it is for beginners to start contributing to the project. Firstly, classify how much detail this file explains regarding beginner contributions, with either NONE, LITTLE, or MUCH detail. Secondly, explain how easy it is for beginners of the project to start contributing, from EASY, MEDIUM, or DIFFICULT. Return your answer as just one sentence for each classification."
        response = ollama.chat(model="llama3:8b", messages=[{"role": "user", "content": query}])
        
        response_text = response['message']['content']

        if "MUCH" in response_text:
            if "HARD" in response_text:
                best_score = max(best_score, 1)
            elif "MEDIUM" in response_text:
                best_score = max(best_score, 3)
            elif "EASY" in response_text:
                best_score = max(best_score, 5)

    beginner_issues = check_beginner_friendly_issues(full_name)
    if beginner_issues == 0:
        beg_issue_score = 0
    elif beginner_issues == 1:
        beg_issue_score = 1
    elif beginner_issues == 2:
        beg_issue_score = 3
    elif beginner_issues == 3:
        beg_issue_score = 4
    else:
        beg_issue_score = 5

    maintainer_response_list = check_maintainer_responsiveness(full_name)
    if len(maintainer_response_list) > 0:
        response_durations = []
    
        for created_at, first_comment_time in maintainer_response_list:
            created_at_dt = datetime.strptime(created_at, "%Y-%m-%dT%H:%M:%SZ")
            first_comment_dt = datetime.strptime(first_comment_time, "%Y-%m-%dT%H:%M:%SZ")
            
            response_time_hours = (first_comment_dt - created_at_dt).total_seconds() / 3600
            response_durations.append(response_time_hours)

        avg_response_time = sum(response_durations) / len(response_durations)

        if avg_response_time < 2:
            maintainer_score = 5
        elif avg_response_time < 5:
            maintainer_score = 4
        elif avg_response_time < 10:
            maintainer_score = 3
        elif avg_response_time < 24:
            maintainer_score = 2
        elif avg_response_time < 48:
            maintainer_score = 1
        else:
            maintainer_score = 0
    else:
        maintainer_score = 0

    score = best_score * 0.5 + beg_issue_score * 0.25 + maintainer_score * 0.25

    return score

def check_beginner_friendly_issues(full_name):
    url = f"https://api.github.com/repos/{full_name}/issues"
    labels = ["good first issue"]
    params = {"labels": ",".join(labels), "state": "open"}
    headers = {
        'Authorization': f'token {github_token}',
        'Accept': 'application/vnd.github.v3+json'
    }

    response = requests.get(url, params=params, headers=headers)
    if response.status_code == 200:
        return len(response.json())
    return 0

def check_maintainer_responsiveness(full_name):
    url = f"https://api.github.com/repos/{full_name}/issues?state=open"
    headers = {
        'Authorization': f'token {github_token}',
        'Accept': 'application/vnd.github.v3+json'
    }
    response = requests.get(url)
    if response.status_code == 200:
        issues = response.json()
        response_times = []
        for issue in issues:
            if "pull_request" not in issue:  # Exclude PRs
                created_at = issue["created_at"]
                comments_url = issue["comments_url"]
                comments_response = requests.get(comments_url, headers=headers)
                if comments_response.status_code == 200 and comments_response.json():
                    first_comment_time = comments_response.json()[0]["created_at"]
                    response_times.append((created_at, first_comment_time))
        return response_times
    return []

print(compute_react84("facebook/react"))
print(compute_react84("flutter/flutter"))
print(compute_react84("facebook/react-native"))
print(compute_react84("tensorflow/tensorflow"))
print(compute_react84("kubernetes/kubernetes"))
print(compute_react84("microsoft/vscode"))
print(compute_react84("beniz/seeks"))
print(compute_react84("gitorious/mainline"))
print(compute_react84("znes/renpass"))