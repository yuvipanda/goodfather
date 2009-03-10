import friendfeed
import friendfeedusers
import sys
import urllib2
from BeautifulSoup import BeautifulSoup, SoupStrainer
import re
import os

username = sys.argv[1]
allex = re.compile(r'(?P<num>\d+) all time')
weekex = re.compile(r'(?P<num>\d+) this week')
def getactivitycount(username):
	prof = urllib2.urlopen('http://friendfeed.com/%s'%username).read()
	node = BeautifulSoup(prof,parseOnlyThese=SoupStrainer('div','synopsis'))
	dat = [x.string.strip('\n') for x in node.findAll('div','synopsis')]
	
	if len(dat) !=2: return (0,0,0,0) #This is actually buggy behavior - if they have just comments or just likes, return 0. Edge case - not worth it. Maybe sometime later, I'll get back to fixing this.
	data = (weekex.search(dat[0]), allex.search(dat[0]),weekex.search(dat[1]),allex.search(dat[1]))
	likesweek = 0 if data[0] == None else data[0].group('num')
	likesall = 0 if data[1] == None  else data[1].group('num')
	commentsweek = 0 if data[2] == None else data[2].group('num')
	commentsall = 0 if data[3] == None else data[3].group('num')

	return (likesweek, likesall, commentsweek, commentsall)

def getuser(username):
	service = friendfeed.FriendFeed()
	user = friendfeedusers.User()
	profile = service._fetch_feed('/api/user/%s/profile'%username)
	
	user.ID = profile['id']
	user.Name = profile['name']
	user.ProfileURL = profile['profileUrl']
	user.NickName = profile['nickname']

	for sub in profile['subscriptions']:
		s = friendfeedusers.Subscription()
		s.ID = sub['id']
		s.Name = sub['name']
		s.NickName = sub['nickname']
		s.URL = sub['profileUrl']
		user.Subscriptions.append(s)
	
	for room in profile['rooms']:
		r = friendfeedusers.Room()
		r.ID = room['id']
		r.Name = room['name']
		r.NickName = room['nickname']
		r.URL = room['url']
		user.Rooms.append(r)
	
	for service in profile['services']:
		s = friendfeedusers.Service()
		s.ID = service['id']
		s.Name = service['name']
		s.ProfileURL = service['profileUrl'] if service.has_key('profileUrl') else ''
		s.IconURL = service['iconUrl']
		user.Services.append(s)
	
	user.LastWeekLikes, user.TotalLikes, user.LastWeekComments, user.TotalComments =  getactivitycount(username)
	return user

if __name__=='__main__':
	ffu = friendfeedusers.FriendFeedUsers(username + '.ffusers.iprogress')
	user = getuser(username)
	count = 0
	for s in user.Subscriptions:
		try:
			ffu.persist(getuser(s.NickName))
			count += 1
			print 'Done ' + str(count) + ' of ' +  str(len(user.Subscriptions))
		except urllib2.HTTPError:			
			print "Private Feed. Skipping"
	os.rename(username + '.ffusers.iprogress', username + '.ffusers')



