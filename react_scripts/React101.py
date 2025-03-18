import requests
import json
import re
import sys
from typing import Optional, Dict
import os
from dotenv import load_dotenv


load_dotenv()
token = os.getenv("GITHUB_TOKEN")


def react_101(repo_full_name: str) -> bool:
    

    headers = {"Accept": "application/vnd.github.v3+json"}
    if token:
        headers["Authorization"] = f"token {token}"

   
    outdated_pattern = re.compile(
        r"(outdated|deprecated|stale doc|remove doc|archived|obsolete|marked as old)",
        re.IGNORECASE
    )

    outdated_info_found = False

    
    try:
        readme_url = f"https://api.github.com/repos/{repo_full_name}/readme"
        resp_readme = requests.get(readme_url, headers=headers)

        if resp_readme.status_code == 200:
            file_info = resp_readme.json()
            import base64
            content_encoded = file_info.get("content", "")
            content_decoded = base64.b64decode(content_encoded).decode("utf-8", errors="replace")

            if outdated_pattern.search(content_decoded):
                outdated_info_found = True
                # print(f"[{repo_full_name}] Found references to outdated info in README.md.")
        else:
            # print(f"[{repo_full_name}] README not accessible (HTTP {resp_readme.status_code}).")
            pass
    except Exception as e:
        # print(f"[{repo_full_name}] Error fetching README.md: {e}")
        pass

    if not outdated_info_found:
        try:
            commits_url = f"https://api.github.com/repos/{repo_full_name}/commits?per_page=30"
            resp_commits = requests.get(commits_url, headers=headers)

            if resp_commits.status_code == 200:
                commits_data = resp_commits.json()
                for commit in commits_data:
                    message = commit.get("commit", {}).get("message", "")
                    if outdated_pattern.search(message):
                        outdated_info_found = True
                        # print(f"[{repo_full_name}] Found reference to outdated info in commit: '{message}'")
                        break
            else:
                # print(f"[{repo_full_name}] Could not fetch commits (HTTP {resp_commits.status_code}).")
                pass
        except Exception as e:
            # print(f"[{repo_full_name}] Error checking commits: {e}")
            pass
    if not outdated_info_found:
        try:
            issues_url = f"https://api.github.com/repos/{repo_full_name}/issues?state=all&per_page=20"
            resp_issues = requests.get(issues_url, headers=headers)

            if resp_issues.status_code == 200:
                issues_data = resp_issues.json()
                for issue in issues_data:
                    title = issue.get("title", "")
                    body = issue.get("body", "")
                    combined_text = f"{title} {body}"

                    if outdated_pattern.search(combined_text):
                        outdated_info_found = True
                        # print(f"[{repo_full_name}] Found reference to outdated info in issue #{issue.get('number')}.")
                        break
            else:
                # print(f"[{repo_full_name}] Could not fetch issues (HTTP {resp_issues.status_code}).")
                pass
        except Exception as e:
            # print(f"[{repo_full_name}] Error checking issues: {e}")
            pass

    if not outdated_info_found:
        try:
            pulls_url = f"https://api.github.com/repos/{repo_full_name}/pulls?state=all&per_page=20"
            resp_pulls = requests.get(pulls_url, headers=headers)

            if resp_pulls.status_code == 200:
                pulls_data = resp_pulls.json()
                for pr in pulls_data:
                    pr_title = pr.get("title", "")
                    pr_body = pr.get("body", "")
                    combined_text = f"{pr_title} {pr_body}"

                    if outdated_pattern.search(combined_text):
                        outdated_info_found = True
                        # print(f"[{repo_full_name}] Found reference to outdated info in PR #{pr.get('number')}.")
                        break
            else:
                # print(f"[{repo_full_name}] Could not fetch pull requests (HTTP {resp_pulls.status_code}).")
                pass
        except Exception as e:
            # print(f"[{repo_full_name}] Error checking pull requests: {e}")
            pass

    return outdated_info_found

print(react_101("public-apis/public-apis"))
