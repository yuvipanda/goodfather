requiresextension = 'ffusers'
name = 'Likes and Comments Counter'
description = "Number of Likes and Comments"
author = "Yuvi"
category = "ffuser"
headers = ['NickName','LikesLastWeek', 'LikesAllTime', 'CommentsLastWeek','CommentsAllTime']

def map(obj):
	return {obj.NickName:'\t'.join([str(x) for x in [obj.LastWeekLikes,obj.TotalLikes,obj.LastWeekComments,obj.TotalComments]])}

def reduce(kvp):
	kp = [kvp.Key]
	for k in kvp.Value:
		kp.append(k)
	return kp
