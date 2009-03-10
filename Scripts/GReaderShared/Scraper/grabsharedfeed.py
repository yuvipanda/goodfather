from greadershared import Post, GoogleReaderShared
from datetime import datetime
from BeautifulSoup import BeautifulSoup, SoupStrainer
import urllib2
import re 
import sys

dateregex = re.compile(r'\s(?P<month>\d+)/(?P<day>\d+)/(?P<year>\d+)')
sharedshareregex  = re.compile(r"via (?P<via>\w+)'s shared items")

postsstrainer = SoupStrainer('div','item')
nextpagestrainer = SoupStrainer('div',id='more')



def PostFromNode(post):
	p = Post()
	titlenode = post.find('h2','item-title')
	if titlenode.div.a != None:
		p.Permalink = titlenode.div.a['href']
		p.Title = titlenode.div.a.string
	else:
		p.Title = titlenode.div.string
	infonode = post.find('div','item-info')
	if infonode.a != None:
		p.Source = infonode.a['href']
	else:
		p.Source = infonode.span.string		
	datematch = dateregex.search(str(infonode))
	year = 2000 + int(datematch.group('year'))
	month = int(datematch.group('month'))
	day = int(datematch.group('day'))
	p.Published = datetime(year, month, day)
	p.Content = u'\n'.join([unicode(x) for x in post.find('div','item-body').contents])

	annotation = post.find('div','entry-annotation-body')
	if annotation != None:
		p.Annotation = u''.join([unicode(x) for x in annotation.contents]).replace(u'&ldquo;',u'').replace(u'&rdquo;','')

	return p

def PostsFromSoup(soup):
	posts = []
	postnodes = soup.findAll('div','item')
	for pn in postnodes:
		p = PostFromNode(pn)
		posts.append(p)
	return posts

def NextPageFromSoup(soup):
	morenode =soup.find('div',id='more')
	if morenode == None:
		return None
	else:
		return morenode.a['href']

def PostsFromPageText(text):
	return PostsFromSoup(BeautifulSoup(text,parseOnlyThese=postsstrainer))

def NextPageFromPageText(text):
	return NextPageFromSoup(BeautifulSoup(text,parseOnlyThese=nextpagestrainer))

if __name__ == '__main__':
	url = sys.argv[1]
	filepath = sys.argv[2]
	limit = int(sys.argv[3])
	curpage = url
	curpageno = 0
	postcount = 0
	
	greader = GoogleReaderShared(filepath)
	while True:
		print curpage
		text = urllib2.urlopen(curpage).read()
		posts = PostsFromPageText(text)
		nextpage = NextPageFromPageText(text)
		for p in posts:
			greader.persist(p)
			postcount += 1 
			if postcount > limit: exit()
		if nextpage is None:
			break
		else:
			curpage = nextpage
		curpageno +=1
		print 'Done %d' % curpageno












