requirestemplates = ['Postable']
name = 'Posts Per Day'
description = "Number of Posts per day"
author = "Yuvi"
category = "Basic"
headers=['Date','Posts']
def map(obj):
	return {obj.Published:1}

def reduce(kvp):
	return [kvp.Key, sum(kvp.Value)]
