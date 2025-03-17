import json
from pydriller import Repository
from datetime import datetime, timedelta

def functionality():
    repo_data= r"C:\Users\srijh\Downloads\github_repos.json"
    out_data= "React9_results.json"

    with open(repo_data, 'r', encoding='utf-8') as file:
        repos = json.load(file)

    results = {}
    for repo in repos:
        repo_url = repo['url']
        print(f"Analyzing {repo_url}...")
        results[repo_url] = {'newcomer_access': 0}
        earlier_contributors = set()
        for commit in Repository(path_to_repo=repo_url, since=datetime.now() - timedelta(days=365)).traverse_commits():
            if commit.author.name not in earlier_contributors:
                results[repo_url]['newcomer_access'] += 1  
            earlier_contributors.add(commit.author.name)  

    with open(output_file, "w", encoding='utf-8') as outfile:
        json.dump(results, outfile, indent=4)

    print(f"Output is here '{output_file}'.")
functionality()
