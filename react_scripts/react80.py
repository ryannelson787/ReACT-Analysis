import requests
import base64
import ollama
import git
import os
import random
from urllib.parse import urlparse

'''
ReACT_80: Make governance explicit

Find relevant files and analyze them for explicit governance using LLM's.
'''
def compute_react80(full_name):
    repo_url = f'https://github.com/{full_name}'

    parsed_url = urlparse(repo_url)
    owner = parsed_url.path.split('/')[1]
    repo_name = parsed_url.path.split('/')[2]

    local_url_base = f'repo_folder'
    local_url = f'repo_folder/{repo_name}'

    if not os.path.exists(local_url):
        os.system(f"git clone {repo_url} {local_url}")

    repo = git.Repo(local_url)
    repo.git.checkout(repo.head.commit)

    required_files = {
        "governance.md", "contributing.md", "code_of_conduct.md", "maintainers.md", "readme.md"
    }
    
    repo_files = {file: file.lower() for file in os.listdir(local_url)}
    found_files = {original for original, lower in repo_files.items() if lower in required_files}

    best_score = 0

    for file in found_files:
        with open(local_url + '/' + file, 'r', encoding="utf-8") as file:
            file_contents = file.read()

        query = f"Here is an md file:\n\n{file_contents}\n\nEND OF FILE\n\nThe file you just read is a file in a GitHub project. You are needed in order to determine how well the governance of the project and its organization is detailed. Please answer how well the structure of the development organization is detailed, as either GREAT, GOOD, OK, or NONE. Return your answer with at most one short sentence."
        response = ollama.chat(model="llama3:8b", messages=[{"role": "user", "content": query}])
        
        response_text = response['message']['content']

        if "OK" in response_text:
            best_score = max(best_score, 1)
        elif "OK" in response_text:
            best_score = max(best_score, 2)
        elif "GOOD" in response_text:
            best_score = max(best_score, 3)
        elif "GREAT" in response_text:
            best_score = max(best_score, 4)

    return (len(found_files) + best_score) * 0.1

# print(compute_react80("facebook/react"))
# print(compute_react80("flutter/flutter"))
# print(compute_react80("facebook/react-native"))
# print(compute_react80("tensorflow/tensorflow"))
# print(compute_react80("kubernetes/kubernetes"))
# print(compute_react80("microsoft/vscode"))
# print(compute_react80("beniz/seeks"))
# print(compute_react80("gitorious/mainline"))
# print(compute_react80("znes/renpass"))