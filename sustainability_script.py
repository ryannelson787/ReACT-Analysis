import requests
import datetime
import numpy as np
import os
from dotenv import load_dotenv
import datetime

load_dotenv()
github_token = os.getenv("GITHUB_TOKEN")

GITHUB_TOKEN = github_token
GITHUB_API_URL = "https://api.github.com/repos/"

HEADERS = {"Authorization": f"token {GITHUB_TOKEN}"}

def get_repo_data(owner, repo):
    """
    Fetches general repository information such as:
    - Star count
    - Fork count
    - Whether it's backed by an organization
    """
    url = f"{GITHUB_API_URL}{owner}/{repo}"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        return response.json()
    return None

def get_commit_history(owner, repo):
    """
    Fetches recent commit history and extracts commit dates.
    Used to evaluate:
    - Recent activity
    - Variance in monthly commits
    - Project duration
    """
    url = f"{GITHUB_API_URL}{owner}/{repo}/commits"
    params = {"per_page": 100}  # Fetching the last 100 commits for analysis
    response = requests.get(url, headers=HEADERS)
    
    if response.status_code == 200:
        commits = response.json()
        commit_dates = [datetime.datetime.strptime(commit["commit"]["author"]["date"], "%Y-%m-%dT%H:%M:%SZ") for commit in commits]
        return commit_dates
    return []

def get_contributors(owner, repo):
    """
    Fetches repository contributors and their contribution count.
    Used to determine:
    - Total number of contributors
    - Number of high-frequency contributors (those with >10 commits)
    """
    url = f"{GITHUB_API_URL}{owner}/{repo}/contributors"
    response = requests.get(url, headers=HEADERS)
    
    if response.status_code == 200:
        return response.json()
    return []

def get_releases(owner, repo):
    """
    Fetches the repository's release history.
    Used to determine:
    - Last release date
    - Consistency of releases over time
    """
    url = f"{GITHUB_API_URL}{owner}/{repo}/releases"
    response = requests.get(url, headers=HEADERS)
    
    if response.status_code == 200:
        return response.json()
    return []

def compute_sustainability_score(owner, repo):
    """
    Calculates the sustainability score based on weighted criteria:
    - Recent commits
    - Low variance in commits per month
    - Length of time project has been active
    - Number of committers with high frequency
    - Total number of committers
    - High number of stars and forks
    - Consistency of last version releases
    - Backing by a larger organization
    """
    
    # Fetch all necessary data from GitHub
    repo_data = get_repo_data(owner, repo)
    commit_dates = get_commit_history(owner, repo)
    contributors = get_contributors(owner, repo)
    releases = get_releases(owner, repo)

    if not repo_data:
        print("Failed to fetch repository data.")
        return None

    # Extract repository-wide metrics
    stars = repo_data.get("stargazers_count", 0)
    forks = repo_data.get("forks_count", 0)
    org_backing = 1 if repo_data.get("organization") else 0  # Binary indicator if repo is backed by an organization

    # Analyze commit statistics
    if commit_dates:
        commit_dates.sort()  # Sorting dates in ascending order
        first_commit = commit_dates[-1]  # Earliest commit
        last_commit = commit_dates[0]  # Most recent commit
        project_duration = (last_commit - first_commit).days / 365  # Convert days to years

        # Compute variance in commits per month
        monthly_commit_counts = {}
        for date in commit_dates:
            key = f"{date.year}-{date.month}"  # Grouping commits by month
            monthly_commit_counts[key] = monthly_commit_counts.get(key, 0) + 1
        
        commit_variance = np.var(list(monthly_commit_counts.values())) if len(monthly_commit_counts) > 1 else 0
    else:
        project_duration = 0
        commit_variance = 0

    # Contributor statistics
    total_committers = len(contributors)  # Total number of contributors
    frequent_committers = sum(1 for c in contributors if c.get("contributions", 0) > 10)  # Committers with >10 commits

    # Release statistics
    if releases:
        release_dates = [datetime.datetime.strptime(r["published_at"], "%Y-%m-%dT%H:%M:%SZ") for r in releases if r.get("published_at")]
        if release_dates:
            last_release = max(release_dates)
            time_since_last_release = (datetime.datetime.utcnow() - last_release).days
        else:
            time_since_last_release = float("inf")  # No releases available
    else:
        time_since_last_release = float("inf")  # No releases available

    one_month_ago = datetime.datetime.utcnow() - datetime.timedelta(days=30)
    recent_commits = [date for date in commit_dates if date > one_month_ago]

    # Define weightage for each criterion
    weights = {
        "recent_commits": 0.2,
        "commit_variance": 0.15,
        "project_duration": 0.2,
        "frequent_committers": 0.15,
        "total_committers": 0.1,
        "stars_forks": 0.1,
        "release_consistency": 0.05,
        "org_backing": 0.05
    }

    # Compute the sustainability score (normalized values)
    score = (
        weights["recent_commits"] * (1 if len(recent_commits) > 5 else 0) + 
        weights["commit_variance"] * (1 - (commit_variance / (commit_variance + 1))) +  # Lower variance is better
        weights["project_duration"] * min(1, project_duration / 5) +  # Normalize to max 5 years
        weights["frequent_committers"] * min(1, frequent_committers / 10) +
        weights["total_committers"] * min(1, total_committers / 30) +
        weights["stars_forks"] * min(1, (stars + forks) / 1000) +
        weights["release_consistency"] * (1 if time_since_last_release < 180 else 0) +  # Score boost if released in last 6 months
        weights["org_backing"] * org_backing
    )

    return round(score * 100, 4)  # Convert score to percentage format