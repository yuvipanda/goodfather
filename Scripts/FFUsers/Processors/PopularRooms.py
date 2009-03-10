requiresextension = 'ffusers'
name = 'Rooms Popular among Subscriptions'
description = "Rooms most people user subscribes to belong to"
author = "Yuvi"
category = "ffuser"
headers = ['RoomName','Subscriptions']

def map(obj):
	return dict( ( s.Name, 1) for s in obj.Rooms )

def reduce(kvp):
	return [kvp.Key, sum(kvp.Value)]
