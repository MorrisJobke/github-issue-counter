#!/usr/bin/env python

import github3, json, os.path

from json_helpers import DateTimeEncoder

GITHUB_TOKEN = 'INSERTYOURSECRETGITHUBAPIKEYHERE'
ORG = 'owncloud'
REPO = 'core'
FILENAME_ISSUES = ORG + 'issues.json'

data = {}

if os.path.isfile(FILENAME_ISSUES):
	f = open(FILENAME_ISSUES)
	data = json.load(f)
	f.close()

gh = github3.login(token=GITHUB_TOKEN)

if REPO not in data.keys():
	data[REPO] = {}

for i in gh.iter_repo_issues(ORG, REPO, state='all'):
	data[REPO][i.number] = {
		'created_at': i.created_at,
		'closed_at': i.closed_at,
		'is_pull_request': (i.pull_request is not None)
	}

f = open(FILENAME_ISSUES, 'w')
json.dump(data, f, cls=DateTimeEncoder)
f.close()
