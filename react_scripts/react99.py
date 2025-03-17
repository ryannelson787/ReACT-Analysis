#!/usr/bin/env python
# coding: utf-8

# In[4]:


import requests
# Keep the issue list clean and triaged


def compute_react99(full_name):
    issues_url = f'https://api.github.com/repos/{full_name}/issues?state=all&per_page=100'
    
    response = requests.get(issues_url)
    if response.status_code != 200:
        return 0

    issues = response.json()
    open_issues = sum(1 for issue in issues if issue["state"] == "open")
    closed_issues = sum(1 for issue in issues if issue["state"] == "closed")
    stale_issues = sum(1 for issue in issues if "stale" in [label["name"].lower() for label in issue.get("labels", [])])

    return 1 if closed_issues > open_issues and stale_issues == 0 else 0




# In[ ]:




