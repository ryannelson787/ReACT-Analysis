import requests
import base64
import ollama
from dotenv import load_dotenv
import os

load_dotenv()
github_token = os.getenv("GITHUB_TOKEN")

'''
ReACT_12: Incorporate an open-source license.

Find license link via github api. Quickly analyze whether its open source.
'''
def compute_react12(full_name):
    api_url = f'https://api.github.com/repos/{full_name}/license'

    headers = {
        'Authorization': f'token {github_token}',
        'Accept': 'application/vnd.github.v3+json'
    }

    response = requests.get(api_url, headers=headers)
    if response.status_code != 200:
        return False
    data = response.json()

    license_types = ["MIT", "Apache", "GPL", "BSD", "MPL", "CDDL", "EPL", "GNU"]

    bytes = base64.b64decode(data['content'])
    license = bytes.decode("utf-8")

    query = f"Here is a license for a software project:\n\n{license}\n\nIs this license an open-source license? Respond with either a YES or a NO and a quick justification to your answer!"
    response = ollama.chat(model="llama3:8b", messages=[{"role": "user", "content": query}])
    
    if "YES" in response:
        return True
    elif "NO" in response:
        return False

    for license_type in license_types:
        if license_type in data['license']['name']:
            return True

    return False

# print(compute_react12("facebook/react"))
# print(compute_react12("flutter/flutter"))
# print(compute_react12("facebook/react-native"))
# print(compute_react12("tensorflow/tensorflow"))
# print(compute_react12("kubernetes/kubernetes"))
# print(compute_react12("microsoft/vscode"))
# print(compute_react12("beniz/seeks"))
# print(compute_react12("gitorious/mainline"))
# print(compute_react12("znes/renpass"))