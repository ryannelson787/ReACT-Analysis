import json
import requests
import re
from datetime import datetime, timedelta
from pydriller import Repository
from collections import defaultdict
import ollama
import os
from dotenv import load_dotenv
 
def react_70(full_name):

    load_dotenv()
    token = os.getenv("GITHUB_TOKEN")
    headers = {"Accept": "application/vnd.github.v3+json", "Authorization": f"token {token}"}
    
    repo_url = f"https://api.github.com/repos/{full_name}"

    supported_languages = [".py", ".java", ".cpp", ".js"]
    
    response = requests.get(f"{repo_url}/contents", headers=headers)
    if response.status_code == 200:
        repo_files = [file["download_url"] for file in response.json() if any(file["name"].endswith(ext) for ext in supported_languages)]
    else:
        repo_files = []
    
    source_code = {}
    for url in repo_files:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            source_code[url] = response.text
    
    findings = {}

    for file, content in source_code.items():
        findings[file] = {
            "public_methods": len(re.findall(r"\bpublic\s+\w+\s+\w+\(", content)),  # Java/C++
            "public_vars": len(re.findall(r"\b(public|var)\s+\w+", content)),  # JavaScript/Java
            "python_public_attrs": len(re.findall(r"\bself\.\w+\s*=", content)),  # Python
            "global_vars": len(re.findall(r"\b(global|var)\s+\w+", content)),  # JavaScript/Python
            "suggestions": []
        }

        if findings[file]["public_vars"] > 5:
            findings[file]["suggestions"].append("Too many public variables. Consider using private/protected access.")
        if findings[file]["global_vars"] > 2:
            findings[file]["suggestions"].append("Found unnecessary global variables. Consider encapsulating them inside classes or functions.")
        if findings[file]["public_methods"] > 10:
            findings[file]["suggestions"].append("Too many public methods. Consider reducing the public interface size.")

    
    
    query = f"""Analyze the following source code from a GitHub repository for encapsulation issues.
    Public Methods Count: {sum(f["public_methods"] for f in findings.values())}.
    Public Variables Count: {sum(f["public_vars"] for f in findings.values())}.
    Global Variables Count: {sum(f["global_vars"] for f in findings.values())}.
    Here are some key findings from the source code: {findings}
    Based on your analysis, just reply with a True if the repository enforces 
    1. proper encapsulation principles
    2. reducing public variables
    3. limiting the public interface
    4. using private/protected attributes where appropriate 
    and False otherwise. Remember, only reply with True or False."""
    response = ollama.chat(model="llama3:8b", messages=[{"role": "user", "content": query}])

    return response['message']['content']

# print(react_70("public-apis/public-apis")) 

