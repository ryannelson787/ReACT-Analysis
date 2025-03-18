import requests
import ollama
import base64

def compute_react31(full_name):
    api_url_readme = f'https://api.github.com/repos/{full_name}/readme'
    api_url_contributing = f'https://api.github.com/repos/{full_name}/contents/CONTRIBUTING.md'

    response_readme = requests.get(api_url_readme)
    response_contributing = requests.get(api_url_contributing)

    readme_content = ""
    contributing_content = ""

    if response_readme.status_code == 200:
        response_readme_json = response_readme.json()
        if "content" in response_readme_json:
            readme_content = base64.b64decode(response_readme_json["content"]).decode("utf-8")

    if response_contributing.status_code == 200:
        response_contributing_json = response_contributing.json()
        if "content" in response_contributing_json:
            contributing_content = base64.b64decode(response_contributing_json["content"]).decode("utf-8")

    documentation = f"README:\n{readme_content}\n\nCONTRIBUTING.md:\n{contributing_content}"

    query = f"Here is a project's documentation:\n\n{documentation}\n\nDoes this documentation provide clear guidance for potential contributors? Respond with either a YES or a NO and nothing else!"
    
    response = ollama.chat(model="llama2:7b", messages=[{"role": "user", "content": query}])

    if "YES" in response.get("message", {}).get("content", "").strip():
        return 1
    else:
        return 0
