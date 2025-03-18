import requests
import re
from datetime import datetime, timedelta
import ollama
import os
from dotenv import load_dotenv
 
def react_78(full_name):

    load_dotenv()
    token = os.getenv("GITHUB_TOKEN")
    headers = {"Accept": "application/vnd.github.v3+json", "Authorization": f"token {token}"}
    
    repo_url = f"https://api.github.com/repos/{full_name}"

    comment_patterns = {
        "python": r"#.*|'''(?:.*?)'''|\"\"\"(?:.*?)\"\"\"",
        "javascript": r"//.*|/\*(?:.*?)\*/",
        "java": r"//.*|/\*(?:.*?)\*/",
        "c": r"//.*|/\*(?:.*?)\*/",
        "cpp": r"//.*|/\*(?:.*?)\*/"
    }
    
    supported_languages = [".py", ".java", ".cpp", ".js", ".c"]
    
    response = requests.get(f"{repo_url}/contents", headers=headers)
    if response.status_code == 200:
        repo_files = [file["download_url"] for file in response.json() if any(file["name"].endswith(ext) for ext in supported_languages)]
    else:
        repo_files = []
    
    source_code = {}
    for url in repo_files:
        if url != None:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                source_code[url] = response.text

    comment_data = {}

    for file, content in source_code.items():
        file_ext = file.split('.')[-1]
        if file_ext == "py":
            lang = "python"
        elif file_ext == "js":
            lang = "javascript"
        elif file_ext == "java":
            lang = "java"
        elif file_ext in ["c", "cpp"]:
            lang = "c"

        comment_matches = re.findall(comment_patterns.get(lang, ""), content, re.DOTALL)
        comments = []
        for match in comment_matches:
            if isinstance(match, tuple): 
                comments.extend([m.strip() for m in match if m]) 
            elif isinstance(match, str):
                comments.append(match.strip()) 

        # Calculate comment ratio
        num_lines = len(content.split("\n"))
        num_comment_lines = sum(len(c.split("\n")) for c in comments)
        comment_ratio = num_comment_lines / num_lines if num_lines > 0 else 0

        comment_data[file] = {
            "comments": comments,
            "comment_ratio": round(comment_ratio, 2)
        }

    
    since_date = (datetime.now() - timedelta(days=30)).isoformat()
    params = {"since": since_date}
    response = requests.get(f"{repo_url}/commits", headers=headers, params=params)
    
    if response.status_code == 200:
        recent_commits = response.json()
    else:
        recent_commits = []

    comment_updates = 0
    total_commits = len(recent_commits)
    for commit in recent_commits:
        commit_message = commit["commit"]["message"].lower()
        if "comment" in commit_message or "docs" in commit_message or "documentation" in commit_message:
            comment_updates += 1

    commit_analysis = {
        "total_commits": total_commits,
        "comment_related_commits": comment_updates,
        "update_ratio": round(comment_updates / total_commits, 2) if total_commits > 0 else 0
    }
    
    query = f"""Analyze the use and update of code comments in a GitHub repository.
    Comment Ratio Per File: {comment_data}
    Total Commits Analyzed: {commit_analysis["total_commits"]}
    Commits Related to Comment Updates: {commit_analysis["comment_related_commits"]}
    Comment Update Ratio: {commit_analysis["update_ratio"]}

    Based on your analysis, just reply with a True if the repository ensures
    1. there are sufficient comments in the code
    2. the comments are relevant and properly formatted (e.g., docstrings, inline comments)
    3. the comments have been updated along with code changes
    4. there are not any outdated comments
    and False otherwise. Remember, only reply with True or False."""

    response = ollama.chat(model="llama3:8b", messages=[{"role": "user", "content": query}])
    return response['message']['content']


# print(react_78("public-apis/public-apis"))

