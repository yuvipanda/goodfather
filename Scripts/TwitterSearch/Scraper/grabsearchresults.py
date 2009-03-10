import simplejson as json
from twittersearch import Tweet, TwitterSearch
from urllib2 import urlopen
from dateutil import parser
from datetime import datetime
from urllib import urlencode
import sys

def TweetFromNode(node):
	t = Tweet()
	t.Text = node['text']
	t.Language = node.get('iso_language_code')
	t.Author = node['from_user']
	t.ID = str(node['id'])
	t.AuthorID = str(node['from_user_id'])
	t.IconURL = node['profile_image_url']
	t.Published = parser.parse(node['created_at'])
	return t

if __name__ == '__main__':
	filename = sys.argv[1]
	searchterm = ' '.join(sys.argv[2:]).replace('\\','')
	url = "http://search.twitter.com/search.json?" + urlencode({"q":searchterm,"rpp":100})

	ts = TwitterSearch(filename)
	count = 0

	while True:
		print url
		results = json.loads(urlopen(url).read())
		tweets = [TweetFromNode(x) for x in results['results']]
		for t in tweets:
			ts.persist(t)
			count += 1
			if count % 10 == 0:
				print "Done %s Tweets" % count
		if not results.has_key('next_page'):
			break 
		url = 'http://search.twitter.com/search.json' + results['next_page']


