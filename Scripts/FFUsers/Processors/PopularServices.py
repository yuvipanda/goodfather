requiresextension = 'ffusers'
name = 'Services Popular among Subscriptions'
description = "Services most added to by people user subscribes to"
author = "Yuvi"
category = "ffuser"
headers = ['ServiceName','Subscriptions']

def map(obj):
	return dict( ( s.Name, 1) for s in obj.Services )

def reduce(kvp):
	return [kvp.Key, sum(kvp.Value)]
