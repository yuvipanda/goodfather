from Blog import Post, Comment
from datetime import datetime

scraperName = 'Scobleizer.com'
scraperAuthor = 'Yuvi'
scraperType = "PostsComments"

def CommentFromCommentNode(commentNode):
        c = Comment()
        c.Title = ""
        authorNode = commentNode.find('cite')
        c.Author = ''.join([unicode(x) for x in authorNode.contents])
        if authorNode.a != None:
        	c.AuthorLink = authorNode.a['href']
          			
        c.Content = u'\n'.join([unicode(x) for x in commentNode.find('p').contents]).strip()
        c.Permalink = commentNode.find('small','commentmetadata').a['href']
        return c
        
def CommentsFromSoup(soup):
	commentList = soup.find('ol','commentlist')
	if commentList == None: return [] #If there are no comments for the post (unlikely, btw :P), just return an empty list. 
	commentNodes = commentList.findAll('li')
	return [CommentFromCommentNode(cN) for cN in commentNodes]

def PostFromSoup(soup, permalink):
	p = Post()
	p.Content = u'\n'.join([unicode(x) for x in soup.find('div','entry').contents]).strip()
	p.Title = soup.find('h2').string
	p.Author = u'Scobleizer'
	p.Permalink = permalink

	permalinkParts = permalink.split('/')
	p.Published = datetime(int(permalinkParts[3]),int(permalinkParts[4]),int(permalinkParts[5]))
	
	p.Tags = [t.string for t in soup.findAll('a',rel='category tag')]	
	return p
	
def CommentPageURLsFromSoup(soup, permalink):
	return [permalink]
	
def PermalinksFromSoup(soup):	
	titlesNodes = soup.findAll('a', rel='bookmark')
	if titlesNodes == None:
		return None
	titles = []
	for title in titlesNodes:
		titles.append(title['href'])
	return titles

def PageURLGenerator():
	pageNo = 0
	while True:
		pageNo = pageNo + 1
		yield "http://scobleizer.com/page/" + str(pageNo)
