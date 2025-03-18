import requests
import json
import re
import sys
from typing import Optional, Dict
import os
from dotenv import load_dotenv
load_dotenv()
token = os.getenv("GITHUB_TOKEN")

def react_89(repo_full_name: str) -> bool:
    headers = {"Accept": "application/vnd.github.v3+json"}
    if token:
        headers["Authorization"] = f"token {token}"


    freedom_pattern = re.compile(
        r"(welcome new|feedback|opinions|propos(e|ing) changes|express viewpoint|comfortable environment|encourag(e|ing) new)",
        re.IGNORECASE
    )

    newcomer_freedom_found = False
    try:
        coc_url = f"https://api.github.com/repos/{repo_full_name}/contents/CODE_OF_CONDUCT.md"
        resp_coc = requests.get(coc_url, headers=headers)
        if resp_coc.status_code == 200:
            import base64
            file_info = resp_coc.json()
            content_encoded = file_info.get("content", "")
            content_decoded = base64.b64decode(content_encoded).decode("utf-8", errors="replace")

            if freedom_pattern.search(content_decoded):
                newcomer_freedom_found = True
                # print(f"[{repo_full_name}] CODE_OF_CONDUCT.md suggests newcomer freedom.")
    except Exception as e:
        # print(f"[{repo_full_name}] Error reading CODE_OF_CONDUCT.md: {e}")
        pass

    if not newcomer_freedom_found:
        try:
            contrib_url = f"https://api.github.com/repos/{repo_full_name}/contents/CONTRIBUTING.md"
            resp_contrib = requests.get(contrib_url, headers=headers)
            if resp_contrib.status_code == 200:
                import base64
                file_info = resp_contrib.json()
                content_encoded = file_info.get("content", "")
                content_decoded = base64.b64decode(content_encoded).decode("utf-8", errors="replace")

                if freedom_pattern.search(content_decoded):
                    newcomer_freedom_found = True
                    # print(f"[{repo_full_name}] CONTRIBUTING.md encourages newcomer freedom.")
        except Exception as e:
            # print(f"[{repo_full_name}] Error reading CONTRIBUTING.md: {e}")
            pass

    if not newcomer_freedom_found:
        try:
            issues_url = f"https://api.github.com/repos/{repo_full_name}/issues?state=all&per_page=20"
            resp_issues = requests.get(issues_url, headers=headers)
            if resp_issues.status_code == 200:
                issues_data = resp_issues.json()
                for issue in issues_data:
                    title = issue.get("title", "")
                    body = issue.get("body", "")
                    if freedom_pattern.search(title) or freedom_pattern.search(body):
                        newcomer_freedom_found = True
                        # print(f"[{repo_full_name}] Found newcomer-friendly reference in issue #{issue.get('number')}.")
                        break
            else:
                # print(f"[{repo_full_name}] Could not fetch issues (HTTP {resp_issues.status_code}).")
                pass
        except Exception as e:
            # print(f"[{repo_full_name}] Error checking issues: {e}")
            pass
    if not newcomer_freedom_found:
        try:
            pulls_url = f"https://api.github.com/repos/{repo_full_name}/pulls?state=all&per_page=20"
            resp_pulls = requests.get(pulls_url, headers=headers)
            if resp_pulls.status_code == 200:
                pulls_data = resp_pulls.json()
                for pr in pulls_data:
                    pr_title = pr.get("title", "")
                    pr_body = pr.get("body", "")
                    if freedom_pattern.search(pr_title) or freedom_pattern.search(pr_body):
                        newcomer_freedom_found = True
                        # print(f"[{repo_full_name}] Found newcomer-friendly reference in PR #{pr.get('number')}.")
                        break
            else:
                # print(f"[{repo_full_name}] Could not fetch pull requests (HTTP {resp_pulls.status_code}).")
                pass
        except Exception as e:
            # print(f"[{repo_full_name}] Error checking pull requests: {e}")
            pass

    return newcomer_freedom_found
print(react_89("public-apis/public-apis"))