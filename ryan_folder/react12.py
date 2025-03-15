import requests
import base64
import ollama

'''
ReACT_12: Incorporate an open-source license.

Find license link via github api. Quickly analyze whether its open source.
'''
def compute_react12(full_name):
	api_url = f'https://api.github.com/repos/{full_name}/license'

	response = requests.get(api_url)
	data = response.json()

	license_types = ["MIT", "Apache", "GPL", "BSD", "MPL", "CDDL", "EPL", "GNU"]

	bytes = base64.b64decode(data['content'])
	license = bytes.decode("utf-8")

	for i in range(3):
		query = f"Here is a license for a software project:\n\n{license}\n\nIs this license an open-source license? Respond with either a YES or a NO and a quick justification to your answer!"
		response = ollama.chat(model="llama2:7b", messages=[{"role": "user", "content": query}])
		
		if "YES" in response:
			return 1
		elif "NO" in response:
			return 0

	for license_type in license_types:
		if license_type in data['license']['name']:
			return 1

	return 0

print(compute_react12("komodorio/helm-dashboard"))