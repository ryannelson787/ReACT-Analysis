import json
from pydriller import Repository
from datetime import datetime, timedelta

def functionality(repo_data, output_file):
    with open(repo_data, 'r', encoding='utf-8') as file:
        repos = json.load(file)
    keywords = {
        'documentation_updates': ['docs', 'documentation', 'readme', 'wiki'],
        'mentorship_activities': ['mentor', 'mentee', 'onboarding', 'training'],
        'community_engagement': ['community', 'contributing', 'code of conduct', 'welcome']
    }
    results_obtained = {}
    for repo in repos:
        repo_url = repo.get('url')
        if not repo_url:
            continue
        print(f"Analyzing repos: {repo_url}...")
        results_obtained[repo_url] = {
            'documentation_updates': [],
            'mentorship_activities': [],
            'community_engagement': []
        }
        try:
            for commit in Repository(path_to_repo=repo_url).traverse_commits():
                commit_message = commit.msg.lower()
                for category, kw_list in keywords.items():
                    if any(kw in commit_message for kw in kw_list):
                        results_obtained[repo_url][category].append({
                            'commit_hash': commit.hash,
                            'author': commit.author.name,
                            'date': commit.author_date.strftime('%Y-%m-%d %H:%M:%S'),
                            'message': commit.msg
                        })
        except Exception as e:
            print(f"Error found in{repo_url}: {e}")
            results_obtained[repo_url]['error'] = str(e)
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results_obtained, f, indent=4)

    print(f" Results saved to {output_file}")

if __name__ == "__main__":
    repo_data = r"C:\Users\srijh\Downloads\github_repos.json" 
    output_file = "react81_results.json"  
    functionality(repo_data, output_file)
