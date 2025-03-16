from pydriller import Repository
from datetime import timedelta, datetime, timezone
from urllib.parse import urlparse
from collections import defaultdict
import lizard
import git
import os

'''
ReACT_28: Maintain a well-structured design.

This ReACT script development was aided by the use of ChatGPT.
'''
def compute_react28(full_name):
    repo_url = f'https://github.com/{full_name}'

    parsed_url = urlparse(repo_url)
    owner = parsed_url.path.split('/')[1]
    repo_name = parsed_url.path.split('/')[2]

    local_url_base = f'repo_folder'
    local_url = f'repo_folder/{repo_name}'

    if not os.path.exists(local_url):
        os.system(f"git clone --depth=1 {repo_url} {local_url}")

    repo = git.Repo(local_url)
    repo.git.checkout(repo.head.commit)

    source_files = get_source_files(local_url)
        
    file_complexity = {}
    file_size = {}
    file_functions = {}
    import_counts = {}
    directory_depths = []

    for filepath in source_files:
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            code = f.readlines()

        analysis = lizard.analyze_file(filepath)
        file_complexity[filepath] = sum(f.cyclomatic_complexity for f in analysis.function_list) / len(analysis.function_list) if analysis.function_list else 0
        file_size[filepath] = sum(1 for line in code if line.strip())
        file_functions[filepath] = len(analysis.function_list)

        import_counts[filepath] = sum(1 for line in code if line.strip().startswith(("import", "from", "#include")))

        directory_depths.append(filepath[len(local_url):].count(os.sep))
            
    num_files = len(source_files)
    avg_complexity = sum(file_complexity.values()) / num_files if num_files else 0
    avg_file_size = sum(file_size.values()) / num_files if num_files else 0
    avg_functions_per_file = sum(file_functions.values()) / num_files if num_files else 0
    avg_imports_per_file = sum(import_counts.values()) / num_files if num_files else 0
    avg_directory_depth = sum(directory_depths) / num_files if num_files else 0

    # print(f"Total Source Code Files: {num_files}")
    # print(f"Avg Complexity per File: {avg_complexity:.2f}")
    # print(f"Avg File Size (LOC): {avg_file_size:.2f}")
    # print(f"Avg Functions per File: {avg_functions_per_file:.2f}")
    # print(f"Avg Imports per File: {avg_imports_per_file:.2f}")
    # print(f"Avg Directory Depth: {avg_directory_depth:.2f}")

    score = avg_complexity + avg_file_size / 200 + avg_functions_per_file / 100 + avg_imports_per_file / 10

    return score

def get_source_files(root_dir, valid_extensions=None):
    if valid_extensions is None:
        valid_extensions = {".py", ".java", ".js", ".ts", ".cpp", ".c", ".hpp", ".h", ".go", ".rs"}
    
    source_files = []
    for root, _, files in os.walk(root_dir):
        for file in files:
            if any(file.endswith(ext) for ext in valid_extensions):
                source_files.append(os.path.join(root, file))
    return source_files

# print(compute_react28("facebook/react"))
# print(compute_react28("flutter/flutter"))
# print(compute_react28("facebook/react-native"))
# print(compute_react28("tensorflow/tensorflow"))
# print(compute_react28("kubernetes/kubernetes"))
print(compute_react28("microsoft/vscode"))
print(compute_react28("beniz/seeks"))
print(compute_react28("gitorious/mainline"))
print(compute_react28("znes/renpass"))