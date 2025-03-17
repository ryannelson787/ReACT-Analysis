import json
from pydriller import Repository
from datetime import datetime, timedelta

def functionality(repo_data, output_file):
    with open(repo_data, 'r', encoding='utf-8') as file:
        repos = json.load(file)
    keywords = {
        'error_messages': ['error message', 'exception', 'fail'],
        'logging': ['log', 'logging', 'logger'],
        'coding_standards': ['style', 'format', 'PEP8', 'lint'],
        'static_analysis': ['pylint', 'flake8', 'sonarqube', 'static analysis']
    }
    cleanup_info = {}
    for repo in repos:
        repo_url = repo.get('url')  
        if not repo_url:
            continue

        print(f"Analyzing repos: {repo_url}...")
        cleanup_info[repo_url] = {
            'error_messages': [],
            'logging': [],
            'coding_standards': [],
            'static_analysis': []
        }
        try:
            for commit in Repository(path_to_repo=repo_url).traverse_commits():
                commit_message = commit.msg.lower()
                for category, kw_list in keywords.items():
                    if any(kw in commit_message for kw in kw_list):
                        cleanup_info[repo_url][category].append({
                            'commit_hash': commit.hash,
                            'author': commit.author.name,
                            'date': commit.author_date.strftime('%Y-%m-%d %H:%M:%S'),
                            'message': commit.msg
                        })
        except Exception as e:
            print(f"Error found in{repo_url}: {e}")
            cleanup_info[repo_url]['error'] = str(e)
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(cleanup_info, f, indent=4)
    print(f"Results  are saved to {output_file}")
if __name__ == "__main__":
    repo_data = r"C:\Users\srijh\Downloads\github_repos.json" 
    out_data= "react73_results.json"  
    functionality(repo_data, out_data)
