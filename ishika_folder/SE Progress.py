#!/usr/bin/env python
# coding: utf-8

# In[2]:


import requests
import json

#GITHUB_USERNAME = "redacted"
#GITHUB_TOKEN = "redacted"

URL = f"https://api.github.com/users/{GITHUB_USERNAME}/repos"
headers = {"Authorization": f"token {GITHUB_TOKEN}"}

response = requests.get(URL, headers=headers)

if response.status_code == 200:
    repos = response.json()
    with open("github_repos.json", "w") as file:
        json.dump(repos, file, indent=4)
    print("Repository data saved successfully!")
else:
    print(f"Error {response.status_code}: {response.text}")


# In[6]:


import requests
import json

#GITHUB_USERNAME = "redacted"
#GITHUB_TOKEN = "redacted"

URL = f"https://api.github.com/users/{GITHUB_USERNAME}/repos"
headers = {"Authorization": f"token {GITHUB_TOKEN}"}

response = requests.get(URL, headers=headers)

if response.status_code == 200:
    repos = response.json()
    with open("github_repos.json", "w") as file:
        json.dump(repos, file, indent=4)
    print("Repository data saved successfully!")
else:
    print(f"Error {response.status_code}: {response.text}")


# In[ ]:


import requests
import json
import time
from datetime import datetime, timedelta

#BASE_URL = "redacted"
#GITHUB_TOKEN = "redacted"
HEADERS = {"Authorization": f"token {GITHUB_TOKEN}"} if GITHUB_TOKEN else {}

MIN_FORKS = 50
MIN_CONTRIBUTORS = 100
MIN_STARS = 100
MIN_COMMITS = 200
MIN_SIZE = 1000
MAX_AGE_YEARS = 10
RECENT_UPDATE = datetime.now() - timedelta(days=180)

params = {
    "q": f"stars:>{MIN_STARS} forks:>{MIN_FORKS} size:>{MIN_SIZE}",
    "sort": "stars",
    "order": "desc",
    "per_page": 100,
    "page": 1
}

all_repos = []
filtered_repos = []

while True:
    response = requests.get(BASE_URL, params=params, headers=HEADERS)
    if response.status_code == 200:
        data = response.json()
        repos = data.get("items", [])
        if not repos:
            break
        all_repos.extend(repos)
        print(f"Fetched {len(all_repos)} repositories...")
        params["page"] += 1
        time.sleep(1)
    else:
        print(f"Error {response.status_code}: {response.text}")
        break

for repo in all_repos:
    owner, name = repo["owner"]["login"], repo["name"]
    repo_url = repo["html_url"]
    created_at = datetime.strptime(repo["created_at"], "%Y-%m-%dT%H:%M:%SZ")
    updated_at = datetime.strptime(repo["pushed_at"], "%Y-%m-%dT%H:%M:%SZ")

    if (datetime.now() - created_at).days > (MAX_AGE_YEARS * 365):
        continue
    if updated_at < RECENT_UPDATE:
        continue

    contributors_url = f"https://api.github.com/repos/{owner}/{name}/contributors"
    commits_url = f"https://api.github.com/repos/{owner}/{name}/commits"
    pulls_url = f"https://api.github.com/repos/{owner}/{name}/pulls"

    contributors_response = requests.get(contributors_url, headers=HEADERS)
    contributors_count = len(contributors_response.json()) if contributors_response.status_code == 200 else 0

    commits_response = requests.get(commits_url, headers=HEADERS, params={"per_page": 1})
    commits_count = int(commits_response.headers.get("Link", "1").split(",")[-1].split("&page=")[-1].split(">")[0]) if commits_response.status_code == 200 else 0

    pulls_response = requests.get(pulls_url, headers=HEADERS)
    pull_requests_count = len(pulls_response.json()) if pulls_response.status_code == 200 else 0

    if (contributors_count >= MIN_CONTRIBUTORS and
        commits_count >= MIN_COMMITS and
        pull_requests_count > 0):
        filtered_repos.append({
            "name": repo["name"],
            "url": repo_url,
            "stars": repo["stargazers_count"],
            "forks": repo["forks_count"],
            "contributors": contributors_count,
            "commits": commits_count,
            "open_pull_requests": pull_requests_count,
            "last_updated": repo["pushed_at"],
            "size_kb": repo["size"]
        })
        print(f"Added: {repo['name']} - {repo_url}")
    time.sleep(1)

with open("filtered_repositories.json", "w") as file:
    json.dump(filtered_repos, file, indent=4)

print(f"\nTotal repositories meeting criteria: {len(filtered_repos)}")

