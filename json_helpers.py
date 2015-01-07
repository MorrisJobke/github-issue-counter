#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json, datetime


class DateTimeEncoder(json.JSONEncoder):
	def default(self, obj):
		if isinstance(obj, datetime.datetime):
			return obj.isoformat()
		elif isinstance(obj, datetime.date):
			return obj.isoformat()
		elif isinstance(obj, datetime.timedelta):
			return (datetime.datetime.min + obj).time().isoformat()
		else:
			return super(DateTimeEncoder, self).default(obj)


def extract_datetime(s):
	if isinstance(s, datetime.datetime):
		return s
	return datetime.datetime.strptime(s[:-3] + s[-2:], '%Y-%m-%dT%H:%M:%S%z')