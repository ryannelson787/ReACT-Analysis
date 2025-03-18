import requests
import json
import re
import sys
from typing import Optional, Dict
import os
from dotenv import load_dotenv
load_dotenv()
token = os.getenv("GITHUB_TOKEN")

def react_81(repo_full_name: str) -> bool:
    headers = {"Accept": "application/vnd.github.v3+json"}
    if token:
        headers["Authorization"] = f"token {token}"
    doc_pattern = re.compile(
        r"(docs?|documentation|wiki|tutorial|guide|knowledge|outdated|update)",
        re.IGNORECASE
    )

    knowledge_up_to_date = False
    try:
        readme_url = f"https://api.github.com/repos/{repo_full_name}/readme"
        resp_readme = requests.get(readme_url, headers=headers)

        if resp_readme.status_code == 200:
            file_info = resp_readme.json()
            import base64
            content_encoded = file_info.get("content", "")
            content_decoded = base64.b64decode(content_encoded).decode("utf-8", errors="replace")
            if doc_pattern.search(content_decoded):
                knowledge_up_to_date = True
                # print(f"[{repo_full_name}] README contains doc-related keywords.")
        else:
            # print(f"[{repo_full_name}] No README or not accessible (HTTP {resp_readme.status_code}).")
            pass
    except Exception as e:
        # print(f"[{repo_full_name}] Error fetching README.md: {e}")
        pass

    if not knowledge_up_to_date:
        try:
            commits_url = f"https://api.github.com/repos/{repo_full_name}/commits?per_page=30"
            resp_commits = requests.get(commits_url, headers=headers)

            if resp_commits.status_code == 200:
                commits_data = resp_commits.json()
                for commit in commits_data:
                    message = commit.get("commit", {}).get("message", "")
                    if doc_pattern.search(message):
                        knowledge_up_to_date = True
                        # print(f"[{repo_full_name}] Found doc-related keyword in commit message: '{message}'")
                        break
            else:
                # print(f"[{repo_full_name}] Could not fetch commits (HTTP {resp_commits.status_code}).")
                pass
        except Exception as e:
            # print(f"[{repo_full_name}] Error checking commits: {e}")
            pass

    if not knowledge_up_to_date:
        try:
            pulls_url = f"https://api.github.com/repos/{repo_full_name}/pulls?state=all&per_page=30"
            resp_pulls = requests.get(pulls_url, headers=headers)

            if resp_pulls.status_code == 200:
                pulls_data = resp_pulls.json()
                for pr in pulls_data:
                    title = pr.get("title", "")
                    if doc_pattern.search(title):
                        knowledge_up_to_date = True
                        # print(f"[{repo_full_name}] Found doc-related keyword in PR title: '{title}'")
                        break
            else:
                # print(f"[{repo_full_name}] Could not fetch pull requests (HTTP {resp_pulls.status_code}).")
                pass
        except Exception as e:
            # print(f"[{repo_full_name}] Error checking pull requests: {e}")
            pass

    return knowledge_up_to_date

print(react_81("public-apis/public-apis"))
