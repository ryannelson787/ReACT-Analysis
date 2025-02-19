from pydriller import Repository
import json
import re
from datetime import datetime, timedelta
from collections import defaultdict

# Repository URL
repo_url = "https://github.com/public-apis/public-apis"

# Keywords related to CI
ci_keywords = ["ci", "workflow", "pipeline", "travis", "jenkins", "github actions", "build", "deploy"]

# Analyze the repository commits
ci_commits = {}
for commit in Repository(repo_url).traverse_commits():
    if any(keyword in commit.msg.lower() for keyword in ci_keywords) or \
       any(file.filename in [".github/workflows/", ".travis.yml", "Jenkinsfile", "circleci/config.yml"]
           for file in commit.modified_files):
        ci_commits[repo_url]= {
            "hash": commit.hash,
            "message": commit.msg,
            "date": commit.committer_date,
            "author": commit.author.name
        }

# Print CI-related commits
# for commit in ci_commits:
#     print(f"Commit: {commit['hash']}\nMessage: {commit['message']}\nDate: {commit['date']}\nAuthor: {commit['author']}\n")

with open("react_6.json", "w") as outfile:
    json.dump(ci_commits, outfile, indent=4, default=str)

print("Contributor analysis completed! Data saved in 'contributors_data.json'")