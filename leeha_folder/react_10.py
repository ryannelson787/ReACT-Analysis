from pydriller import Repository

repo_path = "./AutoGPT/" 
keywords = ["offer job support", "newcomer support", "onboarding"]  

for commit in Repository(repo_path).traverse_commits():
    if any(keyword.lower() in commit.msg.lower() for keyword in keywords):
        print(f"Found in commit: {commit.hash} - {commit.msg}")
        print(f"Author: {commit.author.name}, Date: {commit.author_date}")
        print("Files changed:", [mod.filename for mod in commit.modified_files])
        print("-" * 80)

for commit in Repository(repo_path).traverse_commits():
    for file in commit.modified_files:
        if file.filename.endswith(".jsx") or file.filename.endswith(".tsx") or file.filename.endswith(".js"):
            if "Offer job support" in (file.diff or ""):
                print(f"Possible implementation in commit {commit.hash}: {file.filename}")
                print(f"Author: {commit.author.name}, Date: {commit.author_date}")
                print("-" * 80)

for commit in Repository(repo_path).traverse_commits():
    for file in commit.modified_files:
        if "JobSupport" in file.filename or "offerJobSupport" in (file.diff or ""):
            print(f"Found in {file.filename} in commit {commit.hash}")