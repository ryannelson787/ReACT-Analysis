import json
import requests
import re
from datetime import datetime, timedelta
from pydriller import Repository
from collections import defaultdict
import pytz
import pandas as pd
from concurrent.futures import ThreadPoolExecutor


class TruckFactor:
    def __init__(self, full_name, headers):
        self.full_name = full_name
        self.headers = headers
        self.authorship = defaultdict(lambda: defaultdict(int))
        self.developers = set()
        self.commit_history = []

    def fetch_commits(self, page):
        url = f"https://api.github.com/repos/{self.full_name}/commits"
        response = requests.get(url, headers=self.headers, params={"per_page": 100, "page": page})
        return response.json() if response.status_code == 200 else []

    def get_commit_history(self):
        with ThreadPoolExecutor(max_workers=5) as executor:
            pages = list(range(1, 6))  # Fetch first 5 pages concurrently
            results = executor.map(self.fetch_commits, pages)
        
        for commits in results:
            for commit in commits:
                if commit.get('commit') and commit['commit'].get('author'):
                    author = commit['commit']['author']['email']
                    date = commit['commit']['author']['date']
                    self.commit_history.append((commit['sha'], author, date))
                    self.developers.add(author)
    
    def author_commit_history(self):
        for sha, author, _ in self.commit_history:
            self.authorship[sha][author] += 1
    
    def compute_truck_factor(self):
        file_count = len(self.authorship)
        coverage_threshold = file_count * 0.5  
        author_contributions = defaultdict(int)

        for file, authors in self.authorship.items():
            top_author = max(authors, key=authors.get)
            author_contributions[top_author] += 1

        sorted_authors = sorted(author_contributions, key=author_contributions.get, reverse=True)
        covered_files = 0
        truck_factor = 0
        
        for author in sorted_authors:
            covered_files += author_contributions[author]
            truck_factor += 1
            if covered_files >= coverage_threshold:
                break
        
        return truck_factor, sorted_authors[:truck_factor]
    
    def compute_last_tfdd(self):
        author_last_commit = {}
        latest_commit_time = max(pd.to_datetime([date for _, _, date in self.commit_history]))
        one_year_threshold = timedelta(days=365)
        
        for _, author, date in self.commit_history:
            author_last_commit[author] = pd.to_datetime(date)
        
        tf_devs = self.compute_truck_factor()[1]
        
        last_tfdd = None
        for dev in tf_devs:
            if dev in author_last_commit:
                last_commit_time = author_last_commit[dev]
                if latest_commit_time - last_commit_time > one_year_threshold:
                    last_tfdd = last_commit_time
        
        return last_tfdd

def react_2(full_name):
    
    utc=pytz.UTC

    token = "github_token"
    headers = {"Accept": "application/vnd.github.v3+json", "Authorization": f"token {token}"}

    repo_url = f"https://github.com/{full_name}"
    contributors = defaultdict(lambda: {"first_commit": None, "num_commits": 0, "files_modified": set()})

    tf_calc = TruckFactor(full_name, headers)
    tf_calc.get_commit_history()
    tf_calc.author_commit_history()
    last_tfdd = tf_calc.compute_last_tfdd()

    for commit in Repository(repo_url).traverse_commits():
        author = commit.author.email
        if contributors[author]["first_commit"] is None:
            contributors[author]["first_commit"] = commit.committer_date
        contributors[author]["num_commits"] += 1
        contributors[author]["files_modified"].update(file.filename for file in commit.modified_files)

    new_contributors = {author: data for author, data in contributors.items() if data["first_commit"] > last_tfdd}

    # for author, data in new_contributors.items():
    #     print(f"New Contributor: {author}")
    #     print(f"First Commit Date: {data['first_commit']}")
    #     print(f"Number of Commits: {data['num_commits']}")
    #     print(f"Files Modified: {', '.join(data['files_modified'])}\n")

    return len(new_contributors)

print(react_2("donnemartin/system-design-primer")) 
