import sustainability_script
from urllib.parse import urlparse
import json
import csv

# Path to your JSON file
file_path = 'github_repos.json'

# Open the file and load the data
with open(file_path, 'r') as file:
    data = json.load(file)

csv_file = 'sust_scores.csv'

# Open the CSV file in write mode
with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=["name", "full_name", "score"])

    # Write the header (field names)
    writer.writeheader()

    for repo in data:
        parsed_url = urlparse(repo['full_name'])
        owner = parsed_url.path.split('/')[0]
        repo_name = parsed_url.path.split('/')[1]

        sus_score = sustainability_script.compute_sustainability_score(owner, repo_name)
        repo["score"] = sus_score

        filtered_repo = {key: repo[key] for key in ["name", "full_name", "score"]}

        writer.writerow(filtered_repo)