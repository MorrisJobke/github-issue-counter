#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json, datetime
from json_helpers import extract_datetime

# tweak here the names of the github org and repo to analyse
ORG = 'owncloud'
REPO = 'core'
FILENAME_ISSUES = ORG + 'issues.json'
BUG_LABEL = ['bug']
CRITICAL_BUG_LABEL = ['sev1-critical', 'sev2-high']
APP_LABEL = ['app:dav', 'app:encryption', 'app:federation', 'app:files', 'app:files_encryption', 'app:files_external', 'app:files_trashbin', 'app:files_versions', 'app:objectstore', 'app:provisioning_api', 'app:search', 'app:user_ldap', 'comp:app', 'comp:console-occ', 'comp:core-js', 'comp:core', 'comp:filesystem', 'dev:appframework', 'dev:ocp', 'dev:ocs', 'feature:activity', 'feature:avatars', 'feature:comments', 'feature:federated-cloud-sharing', 'feature:filepicker', 'feature:l10n', 'feature:locking', 'feature:notifications', 'feature:previews', 'feature:quota', 'feature:sharing', 'feature:sidebar', 'feature:tags', 'feature:theming', 'feature:update', 'settings:admin', 'settings:apps', 'settings:installation', 'settings:login', 'settings:personal', 'settings:users']

one_day = datetime.timedelta(days=1)
now = datetime.datetime.now(datetime.timezone.utc)

f = open(FILENAME_ISSUES)
data = json.load(f)
f.close()

if REPO not in data.keys() and len(data[REPO]) == 0:
	raise SystemExit()

# convert all date strings to datetime objects
for i in data[REPO].keys():
	data[REPO][i]['created_at'] = extract_datetime(data[REPO][i]['created_at'])
	if data[REPO][i]['closed_at'] is not None:
		data[REPO][i]['closed_at'] = extract_datetime(data[REPO][i]['closed_at'])

# retrieve highest issue number
last_number = min([int(i) for i in data[REPO].keys()])
first_date = extract_datetime(data[REPO][str(last_number)]['created_at'])

day = datetime.datetime(first_date.year, first_date.month, first_date.day, tzinfo=datetime.timezone.utc)
day += one_day

result = {}

f = open('result.tsv', 'w')
f.write('date\topen_issues\tclosed_issues\topen_prs\tclosed_prs\tranking\t%s\n'%'\t'.join(APP_LABEL))

while day < now:
	key = day.strftime('%Y-%m-%d')
	print(key)

	open_pr_count = 0
	closed_pr_count = 0
	open_issue_count = 0
	closed_issue_count = 0
	rating_number = 0
	rating_apps = {}
	for app in APP_LABEL:
		rating_apps[app] = 0

	for i in data[REPO]:
		element = data[REPO][i]

		if element['created_at'] > day:
			continue

		is_open = True
		if isinstance(element['closed_at'], datetime.datetime) and element['closed_at'] < day:
			is_open = False
		if element['is_pull_request']:
			if is_open:
				open_pr_count += 1
			else:
				closed_pr_count += 1
		else:
			if is_open:
				open_issue_count += 1
			else:
				closed_issue_count += 1

		if is_open:
			rating = 1

			for label in BUG_LABEL:
				if label in element['labels']:
					rating = 10
					break

			for label in CRITICAL_BUG_LABEL:
				if label in element['labels']:
					rating = 100
					break

			rating_number += rating

			for app in APP_LABEL:
				if app in element['labels']:
					rating_apps[app] += rating

	output = '%s\t%i\t%i\t%i\t%i\t%i'%(key, open_issue_count, closed_issue_count, open_pr_count, closed_pr_count, rating_number)

	for app in APP_LABEL:
		output += '\t%i'%rating_apps[app]

	f.write(output + '\n')

	day += one_day

f.close()
