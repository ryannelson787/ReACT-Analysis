import requests
import json
import os
import git
from collections import defaultdict
import pandas as pd
from datetime import datetime, timedelta


class TruckFactor:
    def __init__(self, repo_full_name, headers):
        self.repo_full_name = repo_full_name
        self.headers = headers
        self.authorship = defaultdict(lambda: defaultdict(int))
        self.developers = set()
        self.commit_history = []

    def get_commit_history(self):
        url = f"https://api.github.com/repos/{repo_full_name}/commits"
        page = 1

        while True:
            response = requests.get(url, headers=headers, params={"per_page": 5, "page": page})
            if response.status_code != 200:
                break
            commits = response.json()
            if not commits:
                break
            
            for commit in commits:
                if 'commit' in commit and 'author' in commit['commit'] and commit['commit']['author']:
                    author = commit['commit']['author']['email']
                    date = commit['commit']['author']['date']
                    self.commit_history.append((commit['sha'], author, date))
                    self.developers.add(author)
            
            page += 1
    
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


if __name__ == "__main__":

    #token = "redacted"
    url = "https://api.github.com/search/repositories"

    query = "language:python stars:>100 forks:>50 created:>2015-01-01 size:>1000"
    params = {"q": query, "sort": "stars", "order": "desc", "per_page": 100, "page": 1}  
    headers = {"Accept": "application/vnd.github.v3+json", "Authorization": f"token {token}"}

    ten_years_ago = datetime.now() - timedelta(days=365)
    response = requests.get(url, params=params, headers=headers)
    repos = response.json().get("items", [])

    repo_data = []
    for repo in repos:
        created_at = datetime.strptime(repo["created_at"], "%Y-%m-%dT%H:%M:%SZ")
        updated_at = datetime.strptime(repo["updated_at"], "%Y-%m-%dT%H:%M:%SZ")

        repo_full_name = repo["full_name"] 

        contributors_url = repo["contributors_url"]
        contributors_resp = requests.get(contributors_url, headers=headers)
        contributor_count = len(contributors_resp.json()) if contributors_resp.status_code == 200 else 0

        commits_url = f"https://api.github.com/repos/{repo_full_name}/commits"
        commits_resp = requests.get(commits_url, headers=headers)
        commit_count = len(commits_resp.json()) if commits_resp.status_code == 200 else 0

        prs_url = f"https://api.github.com/repos/{repo_full_name}/pulls?state=all"
        prs_resp = requests.get(prs_url, headers=headers)
        pr_count = len(prs_resp.json()) if prs_resp.status_code == 200 else 0

        issues_url = repo["issues_url"].replace("{/number}", "")
        open_issues_resp = requests.get(f"{issues_url}?state=open", headers=headers)
        open_issues = len(open_issues_resp.json()) if open_issues_resp.status_code == 200 else 0

        closed_issues_resp = requests.get(f"{issues_url}?state=closed", headers=headers)
        closed_issues = len(closed_issues_resp.json()) if closed_issues_resp.status_code == 200 else 0

        total_issues = open_issues + closed_issues
        issue_percentage = (open_issues / total_issues) * 100 if total_issues > 0 else 0 

        tf_calc = TruckFactor(repo_full_name, headers)
        tf_calc.get_commit_history()
        tf_calc.author_commit_history()
        last_tfdd = tf_calc.compute_last_tfdd()

        repo_data.append({
            "name": repo["name"],
            "full_name": repo_full_name,
            "stars": repo["stars_count"],
            "forks": repo["forks_count"],
            "contributors": contributor_count,
            "commits": commit_count,
            "pull_requests": pr_count,
            "size_kb": repo["size"],
            "created_at": repo["created_at"],
            "updated_at": repo["updated_at"],
            "open_issues": open_issues,
            "total_issues": total_issues,
            "issue_percentage": round(issue_percentage, 2),
            "last_tfdd": last_tfdd.strftime("%m/%d/%y %H:%M:%S") if last_tfdd else None,
            "url": repo["html_url"]
        })

    with open("github_repos.json", "w", encoding="utf-8") as file:
        json.dump(repo_data, file, indent=4)

    print(f"Data saved in 'github_repos.json'")
