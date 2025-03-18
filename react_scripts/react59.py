import requests
import ollama
import os
from dotenv import load_dotenv

load_dotenv()
token = os.getenv("GITHUB_TOKEN")

if not token:
    raise ValueError("GitHub token not found. Please set GITHUB_TOKEN in your .env file.")

def compute_react59(full_name):
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
    has_readme = "README.md" in repo_contents
    has_docs = "docs" in repo_contents
    has_tutorials_or_examples = "tutorials" in repo_contents or "examples" in repo_contents

    has_educational_content = False
    if has_readme:
        readme_url = repo_contents["README.md"]["download_url"]
        response = requests.get(readme_url, headers=headers)
        if response.status_code == 200:
            readme_content = response.text
            query = f"Does the following README.md provide clear educational value, tutorials, or guidance for learners?\n\n{readme_content}\n\nRespond with either a YES or a NO and nothing else!"
            ollama_response = ollama.chat(model="llama2:7b", messages=[{"role": "user", "content": query}])

            if ollama_response.get("message", {}).get("content", "").strip() == "YES":
                has_educational_content = True

    return 1 if any([has_readme, has_docs, has_tutorials_or_examples, has_educational_content]) else 0

