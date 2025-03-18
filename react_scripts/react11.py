import requests

def compute_react11(full_name):
    repo_url = f'https://api.github.com/repos/{full_name}'
    response = requests.get(repo_url)

    if response.status_code != 200:
        return 0  

    repo_data = response.json()
    return 1 if repo_data.get("size", float('inf')) < 50000 else 0
