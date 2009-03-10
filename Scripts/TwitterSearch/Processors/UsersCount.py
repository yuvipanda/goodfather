requiresextension = 'tweetssearch'
name = 'Top Authors'
description = "Lists the Authors who tweeted the most"
author = "Yuvi"
category = "tweetssearch"
headers = ['Author','Tweets']

def map(obj):
	return {obj.Author:1}

def reduce(kvp):
	return [kvp.Key, sum(kvp.Value)]
