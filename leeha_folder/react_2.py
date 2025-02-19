import json
import re
from datetime import datetime
from pydriller import Repository
from collections import defaultdict
import pytz

utc=pytz.UTC

with open("github_repos.json", "r") as file:
    repos = json.load(file)

all_repos_data = {}

for repo in repos:
    repo_url = repo["url"]
    contributors = defaultdict(lambda: {"first_commit": None, "num_commits": 0, "files_modified": set()})

    for commit in Repository(repo_url).traverse_commits():
        author = commit.author.email
        if contributors[author]["first_commit"] is None:
            contributors[author]["first_commit"] = commit.committer_date
        contributors[author]["num_commits"] += 1
        contributors[author]["files_modified"].update(file.filename for file in commit.modified_files)

    new_contributors = {author: data for author, data in contributors.items() if utc.localize(data["first_commit"]) > utc.localize(datetime.strptime(repo['last_tfdd'], '%m/%d/%y %H:%M:%S'))}

    for author, data in new_contributors.items():
        print(f"New Contributor: {author}")
        print(f"First Commit Date: {data['first_commit']}")
        print(f"Number of Commits: {data['num_commits']}")
        print(f"Files Modified: {', '.join(data['files_modified'])}\n")

    all_repos_data[repo_url] = new_contributors

with open("react_2.json", "w") as outfile:
    json.dump(all_repos_data, outfile, indent=4, default=str)

print("Data saved in 'react_2.json'")
