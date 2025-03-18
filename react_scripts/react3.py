import requests
# Common programming languages


def compute_react3(full_name):
    repo_url = f'https://api.github.com/repos/{full_name}/languages'
    
    
    common_languages = {
        "Python", "Java", "JavaScript", "TypeScript", "C", "C++", "C#", 
        "Go", "Rust", "Swift", "Ruby", "Kotlin", "PHP", "R", "Perl"
    }

   
    response = requests.get(repo_url)

    if response.status_code != 200:
        return 0  

    languages = response.json()


    return sum(1 for lang in languages.keys() if lang in common_languages)
