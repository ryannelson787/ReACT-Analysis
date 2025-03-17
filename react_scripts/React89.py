import json
from pydriller import Repository

def functionality(repo_data, out_data):
    with open(repo_data, 'r', encoding='utf-8') as file:
        repos = json.load(file)
    keywords = {
        'newcomer_contributions': ['newcomer', 'onboarding', 'first contribution', 'beginner', 'starter'],
        'mentorship': ['mentor', 'mentee', 'guidance', 'coaching', 'support'],
        'project_knowledge_sharing': ['documentation', 'readme', 'wiki', 'contributing'],
        'freedom_to_express': ['suggestion', 'proposal', 'opinion', 'feedback', 'idea', 'refactor']
    }    
    results_obtained= {}   
    for repo in repos:
        repo_url = repo.get('url')
        if not repo_url:
            continue
        print(f"Analyzing repos: {repo_url}...")
        results_obtained[repo_url] = {
            'newcomer_contributions': [],
            'mentorship': [],
            'project_knowledge_sharing': [],
            'freedom_to_express': []
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
            print(f"Errors found in {repo_url}: {e}")
            results_obtained[repo_url]['error'] = str(e)
    with open(out_data, 'w', encoding='utf-8') as f:
        json.dump(results_obtained, f, indent=4)

    print(f"Output is saved to {out_data}")
if __name__ == "__main__":
    repo_data = r"C:\Users\srijh\Downloads\github_repos.json" 
    out_data = "react89_results.json"  
    functionality(repo_data, out_data)
