import requests
import json
import sys
from typing import Optional, Dict
import os
from dotenv import load_dotenv

load_dotenv()
token = os.getenv("GITHUB_TOKEN")


def react_5(repo_full_name: str) -> bool:
   
    headers = {"Accept": "application/vnd.github.v3+json"}
    if token:
        headers["Authorization"] = f"token {token}"

    pull_based_found = False

    try:
        url_pulls = f"https://api.github.com/repos/{repo_full_name}/pulls?state=all&per_page=30"
        response_pulls = requests.get(url_pulls, headers=headers)

        if response_pulls.status_code == 200:
            pulls = response_pulls.json()

            
            if not pulls:
                return False

            for pr in pulls:
                if pr.get("merged_at") is not None:
                    pull_based_found = True
                    # print(f"[{repo_full_name}] Merged PR found: #{pr.get('number')} - {pr.get('title')}")
                    break
            # if not pull_based_found:
                # print(f"[{repo_full_name}] Found PRs, but none are merged.")
        else:
            # print(f"[{repo_full_name}] Could not fetch PRs. HTTP {response_pulls.status_code}")
            pass

    except Exception as e:
        # print(f"[{repo_full_name}] Error checking pull requests: {e}")
        pass

    return pull_based_found

print(react_5("public-apis/public-apis"))
