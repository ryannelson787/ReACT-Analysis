import requests
import json
from datetime import datetime
from pydriller import Repository
from collections import defaultdict


if __name__ == "__main__":
    #TOKEN = "redacted"
    headers = {"Accept": "application/vnd.github.v3+json", "Authorization": f"token {TOKEN}"}

    with open("github_repos.json", "r") as file:
        repos = json.load(file)
    
    all_repos_data = {}

    for repo in repos:
        pr_times = []
        merge_time = defaultdict(lambda: {"max_time": 0.0, "min_time": 0.0, "avg_time": 0.0, "total_prs":0, "total_merges":0})

        repo_url = repo["url"]
        repo_full_name = repo["full_name"] 

        url = f"https://api.github.com/repos/{repo_full_name}/pulls?state=closed&per_page=100"
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            print(f"Failed to get pull requests for {repo_url}")
        
        pull_requests = response.json()
        for pr in pull_requests:
            if pr.get("merged_at"):
                created_at = datetime.strptime(pr["created_at"], "%Y-%m-%dT%H:%M:%SZ")
                merged_at = datetime.strptime(pr["merged_at"], "%Y-%m-%dT%H:%M:%SZ")
                pr_times.append((merged_at - created_at).total_seconds() / 3600) 
        
        if pr_times:
            merge_time["max_time"] = max(pr_times)
            merge_time["min_time"] = min(pr_times)
            avg_merge_time = sum(pr_times) / len(pr_times)
            merge_time["avg_time"] = avg_merge_time
            merge_time["total_prs"] = len(pull_requests)
            merge_time["total_merges"] = len(pr_times)
            
        all_repos_data[repo_url] = merge_time

    with open("react_14.json", "w") as outfile:
        json.dump(all_repos_data, outfile, indent=4)

    print("Data saved in 'react_14.json'")
    