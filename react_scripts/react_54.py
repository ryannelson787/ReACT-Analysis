import json
import requests
import re
from datetime import datetime
from collections import defaultdict
import ollama

def location_to_continent(location):

    query = f"You are an expert at geography, given a location you have to classify the location into one of the 6 continents (Africa, Asia, Australia, Europe, North America, South America) is the {location} is in? Reply in upto atmost two words with just the name of the continent."
    response = ollama.chat(model="llama3:8b", messages=[{"role": "user", "content": query}])

    return response['message']['content']

def react_54(full_name):

    token = "github_token"
    headers = {"Accept": "application/vnd.github.v3+json", "Authorization": f"token {token}"}

    repo_url = f"https://api.github.com/repos/{full_name}/contributors"
    
    response = requests.get(repo_url, headers=headers)

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
    # print(locations)

    continent_counts = defaultdict(int)
    for location in locations:
        
        continent = location_to_continent(location)
        # print(location, continent)
        if continent in ["Africa", "Asia", "Australia", "Europe", "North America", "South America"]:
            continent_counts[continent] += 1
        
    num_continents = sum(1 for count in continent_counts.values() if count > 0)

    print(num_continents)
    
    return num_continents

print(react_54("donnemartin/system-design-primer"))