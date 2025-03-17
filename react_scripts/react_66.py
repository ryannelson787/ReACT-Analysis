import requests
import ollama
 
def react_66(full_name):

    token = "github_token"
    headers = {"Accept": "application/vnd.github.v3+json", "Authorization": f"token {token}"}
    
    repo_url = f"https://api.github.com/repos/{full_name}"

    default_branch = "main"

    test_files = ["tests/", "__tests__/", "test/", "spec/"]
    ci_files = [
        ".github/workflows/",
        ".travis.yml",
        "Jenkinsfile",
        ".circleci/config.yml",
        "azure-pipelines.yml",
        "bitbucket-pipelines.yml",
        "gitlab-ci.yml",
        "circle.yml"
    ]

    coverage_files = [
        "coverage.xml",
        ".coveragerc",
        ".nycrc",
        "coverage/",
        "jest.config.js",
        "karma.conf.js",
        "jacoco.exec",
        "jacoco.xml",
        "cobertura.ser",
        "cobertura.xml",
        ".csproj",
        ".runsettings",
        "opencover.xml",
        ".simplecov",
        "phpunit.xml",
        "php.ini",
        "coverage.out",
        "*.gcov",
        "lcov.info",
        "codecov.yml",
        ".coveralls.yml"
    ]
    
    response = requests.get(f"{repo_url}/contents", headers=headers)
    repo_contents = response.json() if response.status_code == 200 else []

    test_files_found = any(item["name"] in test_files or any(ext in item["name"] for ext in [".test.", ".spec."]) for item in repo_contents)

    response = requests.get(f"{repo_url}/contents/.github/workflows", headers=headers)
    if response.status_code == 200:
        ci_workflows = {item["name"]: requests.get(item["download_url"]).text for item in response.json()}
    else:
        ci_workflows = {}

    response = requests.get(f"{repo_url}/actions/runs", headers=headers)
    if response.status_code == 200:
        runs = response.json().get("workflow_runs", [])
        recent_success = any(run["conclusion"] == "success" for run in runs[:5])
    else:
        recent_success = False

    response = requests.get(f"{repo_url}/branches/{default_branch}/protection", headers=headers)
    if response.status_code == 200:
        rules = response.json()
        required_checks = rules.get("required_status_checks", {}).get("contexts", [])
        branch_protection = any("test" in check.lower() or "ci" in check.lower() for check in required_checks)
    else:
        branch_protection = False
    
    query = f"""Analyze the following GitHub repository to determine if it ensures adequate testing before integrating new features.
    Test files found: {'Yes' if test_files_found else 'No'}. CI/CD workflows present: {'Yes' if ci_workflows else 'No'}
    Recent Successful CI Runs: {'Yes' if recent_success else 'No'}. Branch Protection Requires Tests Before Merge: {'Yes' if branch_protection else 'No'}
    Based on your analysis, just reply with a True if the repo ensures proper testing before merging features, otherwise return False. 
    Here is the repository: {repo_url}. Remember, only reply with True or False."""
    
    response = ollama.chat(model="llama3:8b", messages=[{"role": "user", "content": query}])

    return response['message']['content']

print(react_66("public-apis/public-apis")) 
