#!/usr/bin/env python
# coding: utf-8

# In[3]:


import requests
import ollama

'''
ReACT_67: Clearly communicate unresolved issues.
'''

def compute_react67(full_name):
    
    issues_url = f'https://api.github.com/repos/{full_name}/issues?state=open&labels=needs%20help,bug'
    
 
    response = requests.get(issues_url)
    if response.status_code != 200:
        return 0  
        
    issues = response.json()
    if not issues:
        return 0 


    issue_descriptions = [issue["title"] + "\n" + issue["body"] for issue in issues[:3] if "body" in issue]

    if not issue_descriptions:
        return 0  


    query = f"Analyze the following GitHub issue descriptions and determine if they clearly communicate the unresolved problem:\n\n{issue_descriptions}\n\nRespond with either a YES or a NO and nothing else!"
    ollama_response = ollama.chat(model="llama2:7b", messages=[{"role": "user", "content": query}])

  
    return 1 if "YES" in ollama_response["message"]["content"] else 0




# In[ ]:




