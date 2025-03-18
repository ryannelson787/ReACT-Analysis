import requests
import json
import re
import sys
from typing import Optional, Dict
import os
from dotenv import load_dotenv

load_dotenv()
token = os.getenv("GITHUB_TOKEN")



def react_73(repo_full_name: str) -> bool:

    headers = {"Accept": "application/vnd.github.v3+json"}
    if token:
        headers["Authorization"] = f"token {token}"

    
    cleanup_pattern = re.compile(
        r"(cleanup|refactor|lint|static analysis|error messages|logging improvements)",
        re.IGNORECASE
    )

   
    cleanup_found = False

    try:
        commits_url = f"https://api.github.com/repos/{repo_full_name}/commits?per_page=30"
        resp_commits = requests.get(commits_url, headers=headers)
        if resp_commits.status_code == 200:
            commits_data = resp_commits.json()
            for commit in commits_data:
                message = commit.get("commit", {}).get("message", "")
                if cleanup_pattern.search(message):
                    cleanup_found = True
                    # print(f"[{repo_full_name}] Found cleanup keyword in commit message: '{message}'")
                    break
        else:
            # print(f"[{repo_full_name}] Could not fetch commits. HTTP {resp_commits.status_code}")
            pass
    except Exception as e:
        # print(f"[{repo_full_name}] Error checking commits: {e}")
        pass

    if not cleanup_found:
        try:
            pulls_url = f"https://api.github.com/repos/{repo_full_name}/pulls?state=all&per_page=30"
            resp_pulls = requests.get(pulls_url, headers=headers)
            if resp_pulls.status_code == 200:
                pulls_data = resp_pulls.json()
                for pr in pulls_data:
                    title = pr.get("title", "")
                    if cleanup_pattern.search(title):
                        cleanup_found = True
                        # print(f"[{repo_full_name}] Found cleanup keyword in PR title: '{title}'")
                        break
            else:
                # print(f"[{repo_full_name}] Could not fetch pull requests. HTTP {resp_pulls.status_code}")
                pass
        except Exception as e:
            # print(f"[{repo_full_name}] Error checking pull requests: {e}")
            pass

    return cleanup_found

print(react_73("public-apis/public-apis"))
