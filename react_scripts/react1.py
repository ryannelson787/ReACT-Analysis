import requests
import re
import json
import os
from dotenv import load_dotenv

load_dotenv()
token = os.getenv("GITHUB_TOKEN")


HEADERS = {
    "Accept": "application/vnd.github.v3+json",
    "Authorization": f"token {token}"
}

def react_1(repo_full_name: str) -> bool:
    
    friendly_supportive_found = False
    
    try:
        url_code_of_conduct = f"https://api.github.com/repos/{repo_full_name}/contents/CODE_OF_CONDUCT.md"
        response_coc = requests.get(url_code_of_conduct, headers=HEADERS)

        if response_coc.status_code == 200:
            friendly_supportive_found = True
            #print(f"[{repo_full_name}] Found CODE_OF_CONDUCT.md.")
    except Exception as e:
        print(f"[{repo_full_name}] Error checking CODE_OF_CONDUCT.md: {e}")

    try:
        url_issues = f"https://api.github.com/repos/{repo_full_name}/issues?state=all&per_page=10"
        response_issues = requests.get(url_issues, headers=HEADERS)

        if response_issues.status_code == 200:
            issues = response_issues.json()
            positive_pattern = re.compile(r"\b(thank|thanks|appreciate|welcome|friendly)\b", re.IGNORECASE)

            for issue in issues:
                title = issue.get("title", "")
                body = issue.get("body", "")

                if positive_pattern.search(title) or positive_pattern.search(body):
                    friendly_supportive_found = True
                    #print(f"[{repo_full_name}] Positive language found in issue #{issue.get('number')}: '{title}'")
                    break
        #else:
         #   print(f"[{repo_full_name}] Could not fetch issues. HTTP {response_issues.status_code}")
    except Exception as e:
        print(f"[{repo_full_name}] Error checking issues: {e}")
         
    return friendly_supportive_found

print(react_1("public-apis/public-apis"))
