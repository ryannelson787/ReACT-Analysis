import json
import requests
from datetime import datetime, timedelta

def fetch_pull_requests(owner, repo, token):
    """Fetch pull requests data from GitHub API."""
    headers = {'Authorization': f'token {token}'}
    prs = []
    url = f'https://api.github.com/repos/{owner}/{repo}/pulls?state=all&per_page=100'
    while url:
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            print(f"Failed to fetch data: {response.json()}")
            break
        current_data = response.json()
        if isinstance(current_data, list):
            prs.extend(current_data)
        else:
            print(f"Unexpected data format: {current_data}")
            break
        if 'next' in response.links:
            url = response.links['next']['url']
        else:
            url = None
    return prs

# Load the list of repositories from a JSON file
with open(r"C:\Users\srijh\Downloads\github_repos.json", "r", encoding='utf-8') as file:
    repos = json.load(file)

# Your GitHub token and other config
github_token = 'your_github_token_here'

# Dictionary to store analysis results
repo_analysis = {}

# Analyze each of the first three repositories
for repo in repos[:3]:  # Only process the first three repositories
    owner, repo_name = repo['url'].split('/')[-2:]
    print(f"Analyzing {repo_name} from {owner}...")
    prs = fetch_pull_requests(owner, repo_name, github_token)
    
    # Calculate metrics based on pull requests
    if isinstance(prs, list):
        pr_metrics = {
            'total_prs': len(prs),
            'merged_prs': sum(1 for pr in prs if pr.get('state') == 'closed' and pr.get('merged_at')),
            'closed_prs': sum(1 for pr in prs if pr.get('state') == 'closed' and not pr.get('merged_at')),
            'comment_count': sum(pr.get('comments', 0) for pr in prs),
        }
        repo_analysis[repo['url']] = pr_metrics
        print(f"Pull Request Metrics for {repo_name}: {pr_metrics}\n")
    else:
        print(f"No valid PR data available for {repo_name}")

# Save the results to a JSON file
with open("pull_request_analysis.json", "w", encoding='utf-8') as outfile:
    json.dump(repo_analysis, outfile, indent=4)

print("Analysis completed! The results have been saved in 'pull_request_analysis.json'.")
