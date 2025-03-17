#!/usr/bin/env python
# coding: utf-8

# In[4]:


import requests
import ollama

#Utilize an editing tool that supports compiling and executing code

def compute_react43(full_name):
    
    contents_url = f'https://api.github.com/repos/{full_name}/contents/'

   
    response = requests.get(contents_url)
    if response.status_code != 200:
        return 0  

    repo_contents = {file["name"]: file for file in response.json()}
    has_codespaces_config = ".devcontainer" in repo_contents or "codespace.json" in repo_contents

    
    documentation_files = ["README.md", "docs/"]
    mentions_online_IDE = False

    for doc in documentation_files:
        if doc in repo_contents:
            doc_url = repo_contents[doc]["download_url"]
            response = requests.get(doc_url)
            if response.status_code == 200:
                doc_content = response.text
                query = f"Does the following documentation mention CodeSandbox, Replit, or other online coding tools?\n\n{doc_content}\n\nRespond with either a YES or a NO and nothing else!"
                ollama_response = ollama.chat(model="llama2:7b", messages=[{"role": "user", "content": query}])
                mentions_online_IDE = "YES" in ollama_response["message"]["content"]
                break  

   
    return sum([has_codespaces_config, mentions_online_IDE])



# In[ ]:




