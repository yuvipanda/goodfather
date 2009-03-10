from Blog import Post, Comment
from datetime import datetime
from Network import SoupFromURL

scraperName = 'BoingBoing'
scraperAuthor = 'Yuvi'
scraperType = "PostsOnly"

def PostFromNode(node):
	p = Post()

	p.permalink = node.find('a','permalink')['href']
	permalinkparts = p.permalink.split('/')
	
	p.published = datetime(int(permalinkParts[3]),int(permalinkParts[4]),int(permalinkParts[5]))
	p.author = node.find('span','byline').a.string

	postcontents = node.find('div','entry-body').contents
	p.content = u'\n'.join([unicode(x) for x in postcontents]).strip()

	tagNodes = node.findAll('span','entry-category')
	p.tags = [t.a.string for t in tagNodes]

	p.commentcount = int(node.find('span','entry-footer-comment-count').string)

	return p


def PostsFromPage(soup):
	postNodes = soup.findAll('div','entry')
	return [PostFromNode(node) for node in postNodes]

def PageURLGenerator():
	archivePage = SoupFromURL('http://www.boingboing.net/archives.html')
	archiveLinks = archivePage.findAll('li','archive-list-item')
	for link in archiveLinks:
		yield link.a['href']
