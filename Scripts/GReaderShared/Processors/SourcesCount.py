requiresextension = 'grshared'
name = 'Most Shared Sources'
description = "Counts the Most Shared Sources"
author = "Yuvi"
category = "grshared"
headers = ['Source','Shares']

def map(obj):
	return {obj.Source:1}

def reduce(kvp):
	return [kvp.Key, sum(kvp.Value)]
