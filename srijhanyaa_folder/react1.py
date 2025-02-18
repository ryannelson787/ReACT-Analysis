import json
from datetime import datetime, timedelta
from pydriller import Repository

# Load the list of repositories from a JSON file
with open(r"C:\Users\srijh\Downloads\github_repos.json", "r", encoding='utf-8') as file:
    repos = json.load(file)

# Define the timeframe for active developers (last 90 days)
active_since_date = datetime.now() - timedelta(days=90)

# Dictionary to store analysis results
repo_analysis = {}

# Analyze each of the first three repositories
for repo in repos[:3]:  # Only process the first three repositories
    repo_url = repo["url"]
    contributors = set()
    pr_interaction = []

    # Analyze the repository commits
    for commit in Repository(path_to_repo=repo_url, since=active_since_date).traverse_commits():
        # Add each unique contributor who has committed within the timeframe
        contributors.add(commit.author.email)

        # Check for merge commits to analyze pull request interactions
        if 'Merge pull request' in commit.msg:
            pr_interaction.append({
                'pr_id': commit.hash,
                'author': commit.author.name,
                'comments': len(commit.msg.split('\n'))  # assuming comments are included in commit messages
            })

    # Store the analysis results for the repository
    repo_analysis[repo_url] = {
        'active_contributors': len(contributors),
        'pull_request_interactions': pr_interaction
    }
    print(f"Repository URL: {repo_url}")
    print(f"Number of Active Developers: {len(contributors)}")
    print(f"Pull Request Interactions: {len(pr_interaction)}\n")

# Save the results to a JSON file
with open("active_developers_count.json", "w", encoding='utf-8') as outfile:
    json.dump(repo_analysis, outfile, indent=4)

print("Analysis completed! The results have been saved in 'active_developers_count.json'.")
