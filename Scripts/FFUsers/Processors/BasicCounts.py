requiresextension = 'ffusers'
name = 'Subscriptions, Rooms, Services Counter'
description = "Number of Subscriptions, Rooms, Services"
author = "Yuvi"
category = "ffuser"
headers = ['NickName','Subscriptions', 'Rooms', 'Services']

def map(obj):
	return {obj.NickName:'\t'.join([str(x) for x in [len(obj.Subscriptions),len(obj.Rooms),len(obj.Services)]])}

def reduce(kvp):
	kp = [kvp.Key]
	for k in kvp.Value:
		kp.append(k)
	return kp
