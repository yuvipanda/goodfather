requiresextension = 'tweetssearch'
name = 'Top Languages'
description = "Lists the Languages tweeted the most in"
author = "Yuvi"
category = "tweetssearch"
headers = ['Language','Tweets']

def map(obj):
	return {obj.Language:1}

def reduce(kvp):
	return [kvp.Key, sum(kvp.Value)]
