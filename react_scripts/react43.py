import requests
import ollama
import os
from dotenv import load_dotenv

load_dotenv()
token = os.getenv("GITHUB_TOKEN")

if not token:
    raise ValueError("GitHub token not found. Please set GITHUB_TOKEN in your .env file.")

def compute_react43(full_name):
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "Authorization": f"token {token}"
    }

    contents_url = f'https://api.github.com/repos/{full_name}/contents/'

    response = requests.get(contents_url, headers=headers)
    if response.status_code != 200:
        print(f"Error fetching contents for {full_name}, Status Code: {response.status_code}")
        return 0  

    repo_contents = {file["name"]: file for file in response.json()}
    has_codespaces_config = ".devcontainer" in repo_contents or "codespace.json" in repo_contents

    documentation_files = ["README.md", "docs/"]
    mentions_online_IDE = False

    for doc in documentation_files:
        if doc in repo_contents:
            doc_url = repo_contents[doc]["download_url"]
            response = requests.get(doc_url, headers=headers)
            if response.status_code == 200:
                doc_content = response.text
                query = f"Does the following documentation mention CodeSandbox, Replit, or other online coding tools?\n\n{doc_content}\n\nRespond with either a YES or a NO and nothing else!"
                ollama_response = ollama.chat(model="llama2:7b", messages=[{"role": "user", "content": query}])
                mentions_online_IDE = "YES" in ollama_response.get("message", {}).get("content", "").strip()
                break  

    return sum([has_codespaces_config, mentions_online_IDE])

