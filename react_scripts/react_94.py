import requests
from datetime import datetime, timedelta
import ollama
 
def react_94(full_name):

    token = "github_token"
    headers = {"Accept": "application/vnd.github.v3+json", "Authorization": f"token {token}"}
    
    repo_url = f"https://api.github.com/repos/{full_name}"

    doc_files = ["README.md", "CONTRIBUTING.md", "NEWCOMERS.md", "docs/getting_started.md"]

    response = requests.get(f"{repo_url}/contents", headers=headers)
    if response.status_code == 200:
        try:
            repo_files = {file["name"]: file["download_url"] for file in response.json() if file["name"] in doc_files}
        except:
            return False
    else:
        repo_files = {}
    
    docs = {}
    for name, url in repo_files.items():
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            docs[name] = response.text

    since_date = (datetime.now() - timedelta(days=30)).isoformat()
    params = {"since": since_date}
    response = requests.get(f"{repo_url}/commits", headers=headers, params=params)

    if response.status_code == 200:
        recent_commits = response.json()
    else:
        return False
    
    doc_updates = 0
    total_commits = len(recent_commits)

    for commit in recent_commits:
        commit_message = commit["commit"]["message"].lower()
        if any(keyword in commit_message for keyword in ["docs", "documentation", "readme", "contributing", "newcomers"]):
            doc_updates += 1

    commit_findings = {
        "total_commits": total_commits,
        "doc_related_commits": doc_updates,
        "update_ratio": round(doc_updates / total_commits, 2) if total_commits > 0 else 0
    }
    
    
    query = f"""Analyze the provided GitHub repository's documentation to determine if it includes a clear newcomer-specific page.
    Documentation Files Found: {list(docs.keys())}
    Documentation Content: {docs}
    Total Commits Analyzed: {commit_findings["total_commits"]}
    Commits Related to Documentation Updates: {commit_findings["doc_related_commits"]}
    Update Ratio: {commit_findings["update_ratio"]}

    Based on your analysis, just reply with a True if the repository provides
    1. a dedicated newcomer guide (e.g., `NEWCOMERS.md`, `README.md`, `CONTRIBUTING.md`)
    2. the documentation explains the project structure, important resources (code repo, mailing lists, issue tracker, IRC, code review tools)
    3. the is content well-organized, easy to follow, and up-to-date
    and False otherwise. Remember, only reply with True or False."""

    response = ollama.chat(model="llama3:8b", messages=[{"role": "user", "content": query}])
    return response['message']['content']

print(react_94("donnemartin/system-design-primer")) 
