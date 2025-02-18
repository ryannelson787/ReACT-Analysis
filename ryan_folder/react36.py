from pydriller import Repository
from datetime import timedelta, datetime, timezone
from urllib.parse import urlparse
from collections import defaultdict

'''
ReACT_36: Maintain a small number of core/active developers.

Check over 90 day periods for active contributors (over 5 commits).
See h
'''
def compute_react36(full_name):
	repo_url = f'https://github.com/{full_name}'

	parsed_url = urlparse(repo_url)
	owner = parsed_url.path.split('/')[1]

	local_url_base = f'repo_folder'
	local_url = f'repo_folder/{owner}'

	first_commit = None
	for commit in Repository(repo_url, clone_repo_to=local_url_base).traverse_commits():
		first_commit = commit
		break

	if not first_commit:
		return
	
	first_commit_date = first_commit.committer_date
	last_time_period = first_commit_date
	curr_time_period = first_commit_date + timedelta(days=180)

	contributors = set()
	first_run = True

	while curr_time_period < datetime.now().replace(tzinfo=timezone.utc):
		curr_conts = defaultdict(int)

		commit_count = 0
		for commit in Repository(local_url, since=last_time_period, to=curr_time_period).traverse_commits():
			curr_conts[commit.author.name] += 1
			commit_count += 1

		if first_run:
			for auth in curr_conts:
				if curr_conts[auth] >= 1:
					contributors.add(auth)
		else:
			if commit_count >= 50:
				remove_auths = set()
				for auth in contributors:
					if curr_conts[auth] < 3:
						remove_auths.add(auth)
				contributors -= remove_auths

		last_time_period = curr_time_period
		curr_time_period = curr_time_period + timedelta(days=90)
		first_run = False

	print(contributors)

	

compute_react36("komodorio/helm-dashboard")