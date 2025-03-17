#!/usr/bin/env python
# coding: utf-8

# In[3]:


import requests

def compute_react7(full_name):
    #Maintain well-designed code
    repo_url = f'https://api.github.com/repos/{full_name}/contents/'
    
   
    linting_files = {
        ".pylintrc", ".clang-format", ".eslintrc.json", ".prettierrc", ".stylelintrc",
        ".editorconfig", "flake8", "pylintrc", "checkstyle.xml", ".rubocop.yml"
    }

   
    response = requests.get(repo_url)

    if response.status_code != 200:
        return 0  

    repo_contents = response.json()

   
    found_files_count = sum(1 for file in repo_contents if file['name'] in linting_files)

    return found_files_count  


# In[ ]:




