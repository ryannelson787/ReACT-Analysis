import json
from pydriller import Repository

def functionality(repos_file, out_doc):
    
    
    with open(repos_file, 'r', encoding='utf-8') as file:
        repos = json.load(file)

   
    keywords = ['tutorial', 'documentation', 'docs', 'guide', 'how-to', 'readme', 'example']

    results_obtained = {}

    for repo in repos:
        repo_url = repo.get('url')
        if not repo_url:
            continue

        print(f"Analyzing repos: {repo_url}...")
        tutorial_commits = []
        try:
            for commit in Repository(repo_url).traverse_commits():
                commit_message = commit.msg.lower()
                if any(keyword in commit_message for keyword in keywords):
                    tutorial_commits.append({
                        'commit_hash': commit.hash,
                        'author': commit.author.name,
                        'date': commit.author_date.strftime('%Y-%m-%d %H:%M:%S'),
                        'message': commit.msg
                    })
        except Exception as e:
            print(f"Error processing {repo_url}: {e}")
            results_obtained[repo_url] = {'error': str(e)}
            continue

        
        results_obtained[repo_url] = tutorial_commits

 
    with open(out_doc, 'w', encoding='utf-8') as f:
        json.dump(results_obtained, f, indent=4)

    print(f"Results are saved to {out_doc}")

if __name__ == "__main__":
    repos_file = r"C:\Users\srijh\Downloads\github_repos.json" 
    out_doc = "react97_results.json"  
    functionality(repos_file, out_doc)
