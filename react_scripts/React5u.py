import json
import requests

def functionality(owner, repo):
    prs = []
    url = f'https://api.github.com/repos/{owner}/{repo}/pulls?state=all&per_page=100'

    while url:
        response = requests.get(url)  
        if response.status_code != 200:
            print(f"Failed to fetch{repo}, status code: {response.status_code}")
            break
        current_data = response.json()
        if isinstance(current_data, list):
            prs.extend(current_data)
        else:
            print(f"Unexpected format{repo}")
            break
        url = response.links.get('next', {}).get('url')  

    return prs

def analy_repo():
    repo_data = r"C:\Users\srijh\Downloads\github_repos.json"
    output_file = "react_5_results.json"

    with open(repo_data, "r", encoding='utf-8') as file:
        repos = json.load(file)

    reposito_analysis = {}

    for repo in repos:
        owner, repo_name = repo['url'].split('/')[-2:]
        print(f"Analyzing {repo_name}")

        prs = functionality(owner, repo_name)

        if isinstance(prs, list):
            pr_metrics = {
                'prs_totalno': len(prs),
                'prs_merge': sum(1 for pr in prs if pr.get('state') == 'closed' and pr.get('merged_at')),
                'prs_closed': sum(1 for pr in prs if pr.get('state') == 'closed' and not pr.get('merged_at')),
                'num_of_com': sum(pr.get('comments', 0) for pr in prs),
            }
            reposito_analysis[repo['url']] = pr_metrics
            print(f"PR Metrics for {repo_name}: {pr_metrics}\n")
        else:
            print(f"Invalid info{repo_name}")

    with open(output_file, "w", encoding='utf-8') as outfile:
        json.dump(reposito_analysis, outfile, indent=4)

    print("Done")

analy_repo()
