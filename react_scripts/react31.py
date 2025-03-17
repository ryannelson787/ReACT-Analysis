#!/usr/bin/env python
# coding: utf-8

# In[3]:


import requests
import ollama
import base64
#Offer coding guidelines

def compute_react31(full_name):
	api_url_readme = f'https://api.github.com/repos/{full_name}/readme'
	api_url_contributing = f'https://api.github.com/repos/{full_name}/contents/CONTRIBUTING.md'

	response_readme = requests.get(api_url_readme).json()
	response_contributing = requests.get(api_url_contributing).json()

	readme_content = base64.b64decode(response_readme.get("content", "")).decode("utf-8") if "content" in response_readme else ""
	contributing_content = base64.b64decode(response_contributing.get("content", "")).decode("utf-8") if "content" in response_contributing else ""

	documentation = f"README:\n{readme_content}\n\nCONTRIBUTING.md:\n{contributing_content}"

	query = f"Here is a project's documentation:\n\n{documentation}\n\nDoes this documentation provide clear guidance for potential contributors? Respond with either a YES or a NO and nothing else!"
	response = ollama.chat(model="llama2:7b", messages=[{"role": "user", "content": query}])
	print(response)

	return 1 if "YES" in response else 0



# In[ ]:




