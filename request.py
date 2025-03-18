import requests
import json
import os
import git
from collections import defaultdict
import pandas as pd
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv


if __name__ == "__main__":

    load_dotenv()
    token = os.getenv("GITHUB_TOKEN")
    headers = {"Accept": "application/vnd.github.v3+json", "Authorization": f"token {token}"}

    url = "https://api.github.com/search/repositories"

    query = "language:python stars:>100 forks:>50 created:>2015-01-01 size:>1000"
    params = {"q": query, "sort": "stars", "order": "desc", "per_page": 100, "page": 1}  
    headers = {"Accept": "application/vnd.github.v3+json", "Authorization": f"token {token}"}

    ten_years_ago = datetime.now() - timedelta(days=365)
    response = requests.get(url, params=params, headers=headers)
    print(response)
    repos = response.json().get("items", [])

    repo_data = []
    for repo in repos:

        created_at = datetime.strptime(repo["created_at"], "%Y-%m-%dT%H:%M:%SZ")
        updated_at = datetime.strptime(repo["updated_at"], "%Y-%m-%dT%H:%M:%SZ")

        repo_full_name = repo["full_name"] 

        contributors_url = repo["contributors_url"]
        contributors_resp = requests.get(contributors_url, headers=headers)
        contributor_count = len(contributors_resp.json()) if contributors_resp.status_code == 200 else 0

        commits_url = f"https://api.github.com/repos/{repo_full_name}/commits"
        commits_resp = requests.get(commits_url, headers=headers)
        commit_count = len(commits_resp.json()) if commits_resp.status_code == 200 else 0

        prs_url = f"https://api.github.com/repos/{repo_full_name}/pulls?state=all"
        prs_resp = requests.get(prs_url, headers=headers)
        pr_count = len(prs_resp.json()) if prs_resp.status_code == 200 else 0

        issues_url = repo["issues_url"].replace("{/number}", "")
        open_issues_resp = requests.get(f"{issues_url}?state=open", headers=headers)
        open_issues = len(open_issues_resp.json()) if open_issues_resp.status_code == 200 else 0

        closed_issues_resp = requests.get(f"{issues_url}?state=closed", headers=headers)
        closed_issues = len(closed_issues_resp.json()) if closed_issues_resp.status_code == 200 else 0

        total_issues = open_issues + closed_issues
        issue_percentage = (open_issues / total_issues) * 100 if total_issues > 0 else 0 

        repo_data.append({
            "name": repo["name"],
            "full_name": repo_full_name,
            # "stars": repo["stars"],
            "forks": repo["forks_count"],
            "contributors": contributor_count,
            "commits": commit_count,
            "pull_requests": pr_count,
            "size_kb": repo["size"],
            "created_at": repo["created_at"],
            "updated_at": repo["updated_at"],
            "open_issues": open_issues,
            "total_issues": total_issues,
            "issue_percentage": round(issue_percentage, 2),
            # "last_tfdd": last_tfdd.strftime("%m/%d/%y %H:%M:%S") if last_tfdd else None,
            "url": repo["html_url"],
            "score": repo["score"]
        })

    with open("github_repos.json", "w", encoding="utf-8") as file:
        json.dump(repo_data, file, indent=4)

    print(f"Data saved in 'github_repos.json'")
