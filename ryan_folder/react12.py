import requests
import base64
import ollama

def compute_react12(full_name):
	api_url = f'https://api.github.com/repos/{full_name}/license'

	response = requests.get(api_url)
	data = response.json()

	license_types = ["MIT", "Apache", "GPL", "BSD", "MPL", "CDDL", "EPL", "GNU"]

	bytes = base64.b64decode(data['content'])
	license = bytes.decode("utf-8")

	query = f"Here is a license for a software project:\n\n{license}\n\nIs this license an open-source license? Respond with either a YES or a NO and nothing else!"
	response = ollama.chat(model="codellama:13b", messages=[{"role": "user", "content": query}])
	print(response)

	for license_type in license_types:
		if license_type in data['license']['name']:
			return 1

	return 0

print(compute_react12("nocodb/nocodb"))