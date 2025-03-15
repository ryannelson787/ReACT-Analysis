import requests
import base64
import ollama
import git
import os
import random
from urllib.parse import urlparse

'''
ReACT_72: Improve naming in the source code

Go through each code file, ask LLM how good naming is using key naming conventions.
'''
def compute_react72(full_name):
	repo_url = f'https://github.com/{full_name}'

	parsed_url = urlparse(repo_url)
	owner = parsed_url.path.split('/')[1]
	repo_name = parsed_url.path.split('/')[2]

	local_url_base = f'repo_folder'
	local_url = f'repo_folder/{repo_name}'

	if not os.path.exists(local_url):
		os.system(f"git clone {repo_url} {local_url}")

	repo = git.Repo(local_url)
	repo.git.checkout(repo.head.commit)

	source_files = get_source_files(local_url)
      
	total_num_great = 0
	total_num_good = 0
	total_num_ok = 0
	total_num_poor = 0
	total_num_horrible = 0
      
	iter_count = 0
	for file in source_files:
		iter_count += 1
    
		if iter_count > 10:
			break

		[num_great, num_good, num_ok, num_poor, num_horrible] = get_naming_scores(file)
            
		total_num_great += num_great
		total_num_good += num_good
		total_num_ok += num_ok
		total_num_poor += num_poor
		total_num_horrible += num_horrible
            
		print([total_num_great, total_num_good, total_num_ok, total_num_poor, total_num_horrible])

	return 0

def get_source_files(root_dir, valid_extensions=None):
	if valid_extensions is None:
		valid_extensions = {".py", ".java", ".js", ".ts", ".cpp", ".c", ".hpp", ".h", ".go", ".rs"}
    
	source_files = []
	for root, _, files in os.walk(root_dir):
		for file in files:
			if any(file.endswith(ext) for ext in valid_extensions):
				source_files.append(os.path.join(root, file))
		
	random.shuffle(source_files)
	return source_files

def get_naming_scores(filepath):
	with open(filepath, 'r', encoding="utf-8") as file:
		file_contents = file.read()

	query = f"You are being given a code file. For each name of a class, function, structure, or variable in this file, analyze how well it is named for code readability purposes. Choose between the classifications GREAT, GOOD, OK, POOR, and HORRIBLE for each name. Output your answers in the following format:\n\n1. name: classification, reason\n2. name: classification, reason\n...\n\nHere is the code:\n\n{file_contents}"
	response = ollama.chat(model="llama2:7b", messages=[{"role": "user", "content": query}])
    
	response_text = response['message']['content']

	num_great = response_text.count("GREAT")
	num_good = response_text.count("GOOD")
	num_ok = response_text.count("OK")
	num_poor = response_text.count("POOR")
	num_horrible = response_text.count("HORRIBLE")
	
	return [num_great, num_good, num_ok, num_poor, num_horrible]

print(compute_react72("komodorio/helm-dashboard"))