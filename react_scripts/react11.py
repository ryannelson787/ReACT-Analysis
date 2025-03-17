#!/usr/bin/env python
# coding: utf-8

# In[11]:


import requests

def compute_react11(full_name):
    #Keep the project small and simple

    repo_url = f'https://api.github.com/repos/{full_name}'

  
    response = requests.get(repo_url)


    if response.status_code != 200:
        return False


    repo_data = response.json()


    return repo_data.get("size", float('inf')) < 10000




# In[ ]:




