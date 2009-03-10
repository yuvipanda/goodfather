requiresextension = 'ffusers'
name = 'People Popular among Subscriptions'
description = "People most subscribed to by people user subscribes to"
author = "Yuvi"
category = "ffuser"
headers = ['NickName','Subscriptions']

def map(obj):
	return dict( ( s.NickName, 1) for s in obj.Subscriptions )

def reduce(kvp):
	return [kvp.Key, sum(kvp.Value)]
