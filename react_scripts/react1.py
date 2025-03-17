import json
from datetime import datetime, timedelta
from pydriller import Repository

def functionality():
    repo_data = r"C:\Users\srijh\Downloads\github_repos.json"
    out_data = "react_1_results.json"
    with open(repo_data, "r", encoding='utf-8') as file:
        repos = json.load(file)
    active_since_date = datetime.now() - timedelta(days=90)
    analy_reposito = {}
    for repo in repos:  
        repo_url = repo["url"]
        contrib = set()
        int_prior = []
        for commit in Repository(path_to_repo=repo_url, since=active_since_date).traverse_commits():
            contrib.add(commit.author.email)
            if 'Merge pull request' in commit.msg:
                int_prior.append({
                    'pr_id': commit.hash,
                    'author': commit.author.name,
                    'comments': len(commit.msg.split('\n')) 
                })

        analy_reposito[repo_url] = {
            'active_contributors': len(contrib),
            'pull_request_interactions': int_prior
        }

        print(f"URL of the repo: {repo_url}")
        print(f"Active Dev count: {len(contrib)}")
        print(f"PRI: {len(int_prior)}\n")

    with open(out_data, "w", encoding='utf-8') as outfile:
        json.dump(analy_reposito, outfile, indent=2)
    
    print("Info is saved")
functionality()
