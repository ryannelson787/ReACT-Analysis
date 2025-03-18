import requests
import ollama

def compute_react59(full_name):
    contents_url = f'https://api.github.com/repos/{full_name}/contents/'
    
    response = requests.get(contents_url)
    if response.status_code != 200:
        return 0  

    repo_contents = {file["name"]: file for file in response.json()}
    has_readme = "README.md" in repo_contents
    has_docs = "docs" in repo_contents
    has_tutorials_or_examples = "tutorials" in repo_contents or "examples" in repo_contents

    has_educational_content = False
    if has_readme:
        readme_url = repo_contents["README.md"]["download_url"]
        response = requests.get(readme_url)
        if response.status_code == 200:
            readme_content = response.text
            query = f"Does the following README.md provide clear educational value, tutorials, or guidance for learners?\n\n{readme_content}\n\nRespond with either a YES or a NO and nothing else!"
            ollama_response = ollama.chat(model="llama2:7b", messages=[{"role": "user", "content": query}])

            if ollama_response.get("message", {}).get("content", "").strip() == "YES":
                has_educational_content = True

    return 1 if any([has_readme, has_docs, has_tutorials_or_examples, has_educational_content]) else 0
