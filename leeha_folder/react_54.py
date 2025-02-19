import requests
import json
from collections import defaultdict
from pydriller import Repository

if __name__ == "__main__":

    continent_map = {
    "Africa": ["KE", "GH", "ZA", "NG", "EG", "MA", "DZ", "TN", "SN", "UG"],
    "Asia": ["ID", "SG", "IN", "CN", "JP", "KR", "PH", "TH", "VN", "MY"],
    "Australia": ["AU", "NZ", "FJ", "PG", "WS", "TO"],
    "Europe": ["DE", "UK", "FR", "IT", "NL", "ES", "SE", "NO", "FI", "DK"],
    "North America": ["US", "CA", "MX", "PR", "JM", "TT"],
    "South America": ["BR", "AR", "CL", "CO", "PE", "VE", "UY"],
    }
    
    with open("github_repos.json", "r") as file:
        repos = json.load(file)

    #TOKEN = "redacted"
    headers = {"Accept": "application/vnd.github.v3+json", "Authorization": f"token {TOKEN}"}

    with open("github_repos.json", "r") as file:
        repos = json.load(file)
    
    all_repos_data = {}

    for repo in repos:

        repo_full_name = repo["full_name"] 
        url = f"https://api.github.com/repos/{repo_full_name}/contributors"
        response = requests.get(url, headers=headers)

        locations = set()
        if response.status_code == 200:
            contributors = response.json()
            for contributor in contributors:
                user_url = contributor["url"]
                user_resp = requests.get(user_url, headers=headers)
                if user_resp.status_code == 200:
                    user_data = user_resp.json()
                    location = user_data.get("location", "Unknown")
                    locations.add(location)

        continent_counts = defaultdict(int)
        for location in locations:
            for continent, countries in continent_map.items():
                if any(country in location for country in countries):
                    continent_counts[continent] += 1

            
        num_continents = sum(1 for count in continent_counts.values() if count > 0)
        
        all_repos_data[repo_full_name] = {
            "Continents number": num_continents,
            "Contributor locations": list(locations)
            
        }

    with open("react_54.json", "w") as outfile:
        json.dump(all_repos_data, outfile, indent=4)    
    print("Data saved in 'react_54.json'") 
