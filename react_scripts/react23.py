#!/usr/bin/env python
# coding: utf-8

# In[4]:


import requests
#Tag tasks based on their complexity level

def compute_react23(full_name):

    issues_url = f'https://api.github.com/repos/{full_name}/issues?state=open'

   
    response = requests.get(issues_url)
    if response.status_code != 200:
        return 0 

    issues = response.json()

   
    complexity_labels = {"beginner-friendly", "easy", "complex", "hard"}

   
    has_complexity_tag = any(
        "labels" in issue and any(label["name"].lower() in complexity_labels for label in issue["labels"])
        for issue in issues
    )

   
    return 1 if has_complexity_tag else 0




# In[ ]:




