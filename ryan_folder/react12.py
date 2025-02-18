import requests

def compute_react12(full_name):
  api_url = f'https://api.github.com/repos/{full_name}/license'

  response = requests.get(api_url)
  data = response.json()

  license_types = ["MIT", "Apache", "GPL", "BSD", "MPL", "CDDL", "EPL", "GNU"]

  for license_type in license_types:
    if license_type in data['license']['name']:
      return True

  return False

print(compute_react12("nocodb/nocodb"))