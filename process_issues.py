#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json, datetime
from json_helpers import extract_datetime

# tweak here the names of the github org and repo to analyse
ORG = 'owncloud'
REPO = 'core'
FILENAME_ISSUES = ORG + 'issues.json'

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
f.write('date\topen_issues\tclosed_issues\topen_prs\tclosed_prs\n')

while day < now:
	key = day.strftime('%Y-%m-%d')
	print(key)

	open_pr_count = 0
	closed_pr_count = 0
	open_issue_count = 0
	closed_issue_count = 0

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

	f.write('%s\t%i\t%i\t%i\t%i\n'%(key, open_issue_count, closed_issue_count, open_pr_count, closed_pr_count))

	day += one_day

f.close()