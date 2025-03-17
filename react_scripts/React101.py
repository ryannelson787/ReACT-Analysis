import json
from pydriller import Repository

def functionality(repos_file, output_file):
    with open(repos_file, 'r', encoding='utf-8') as file:
        repos = json.load(file)
    keywords = ['documentation', 'docs', 'readme', 'deprecated', 'obsolete', 'remove', 'update']
    results_obtained = {}
    for repo in repos:
        repo_url = repo.get('url')
        if not repo_url:
            continue
        print(f"Analyzing repos: {repo_url}...")
        doc_commits = []
        try:
            for commit in Repository(repo_url).traverse_commits():
                commit_message = commit.msg.lower()
                if any(keyword in commit_message for keyword in keywords):
                    doc_commits.append({
                        'commit_hash': commit.hash,
                        'author': commit.author.name,
                        'date': commit.author_date.strftime('%Y-%m-%d %H:%M:%S'),
                        'message': commit.msg
                    })
        except Exception as e:
            print(f"Error found in {repo_url}: {e}")
            results_obtained[repo_url] = {'error': str(e)}
            continue
        results_obtained[repo_url] = doc_commits
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results_obtained, f, indent=4)

    print(f"Output is saved to {output_file}")
if __name__ == "__main__":
    repos_file = r"C:\Users\srijh\Downloads\github_repos.json"  
    output_file = "react101_results.json"  
    functionality(repos_file, output_file)
