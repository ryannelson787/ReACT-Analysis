import requests
import json
import re
import sys
from typing import Optional, Dict
import os
from dotenv import load_dotenv
load_dotenv()
token = os.getenv("GITHUB_TOKEN")


def react_9(repo_full_name: str) -> bool:
    
    headers = {"Accept": "application/vnd.github.v3+json"}
    if token:
        headers["Authorization"] = f"token {token}"

    newcomer_access_found = False

    try:
        url_contrib = f"https://api.github.com/repos/{repo_full_name}/contents/CONTRIBUTING.md"
        resp_contrib = requests.get(url_contrib, headers=headers)
        if resp_contrib.status_code == 200:
            file_info = resp_contrib.json()
            import base64
            content_encoded = file_info.get("content", "")
            content_decoded = base64.b64decode(content_encoded).decode("utf-8", errors="replace")
            pattern = re.compile(r"(newcomer|onboarding|direct push|write access|push access)", re.IGNORECASE)
            if pattern.search(content_decoded):
                newcomer_access_found = True
                # print(f"[{repo_full_name}] CONTRIBUTING.md suggests newcomer or direct push access.")
        else:
            # print(f"[{repo_full_name}] No CONTRIBUTING.md or not accessible (HTTP {resp_contrib.status_code}).")
            pass
    except Exception as e:
        # print(f"[{repo_full_name}] Error fetching CONTRIBUTING.md: {e}")
        pass
    try:
        url_collabs = f"https://api.github.com/repos/{repo_full_name}/collaborators?per_page=30"
        resp_collabs = requests.get(url_collabs, headers=headers)

        if resp_collabs.status_code == 200:
            collaborators = resp_collabs.json()
            multiple_collaborators = len(collaborators) > 1

           
            has_pusher = any(
                collab.get("permissions", {}).get("push") or collab.get("permissions", {}).get("admin")
                for collab in collaborators
            )

            if multiple_collaborators and has_pusher:
                newcomer_access_found = True
                # print(f"[{repo_full_name}] Multiple collaborators with push/admin permissions found.")
            elif len(collaborators) == 1:
                # print(f"[{repo_full_name}] Only a single collaborator (likely the owner).")
                pass
            else:
                # print(f"[{repo_full_name}] Collaborators found but no push/admin permissions or insufficient data.")
                pass
        else:
            # print(f"[{repo_full_name}] Could not fetch collaborator list (HTTP {resp_collabs.status_code}).")
            pass
    except Exception as e:
        # print(f"[{repo_full_name}] Error fetching collaborators: {e}")
        pass

    return newcomer_access_found

print(react_9("public-apis/public-apis"))
