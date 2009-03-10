from Blog import Post, Comment
from datetime import datetime

scraperName = 'Desipundit'
scraperAuthor = 'Yuvi'
scraperType = "PostsComments"

def CommentFromCommentNode(commentNode):
        c = Comment()
        c.title = ""
        commentMetaNode = commentNode.find('p','comment-meta')
        if commentMetaNode == None: commentMetaNode = commentNode.find('p','comment-meta ')
        authorNode = commentMetaNode.find('a', rel='external nofollow')
        if authorNode != None:
        	c.author = authorNode.string
         	c.authorLink = authorNode['href']
        else:
        	metaString = u' '.join(str(commentMetaNode.contents))
        	c.author = metaString.split('<br',1)[0]  
			
        c.content = u'\n'.join([unicode(x) for x in commentNode.find('div','comment-body  clearfix').contents]).strip()
        c.permalink = commentNode.find('a',title='Comment permalink')['href']
        return c
        
def CommentsFromSoup(soup):
	return [CommentFromCommentNode(cN) for cN in soup.findAll('div','comment')]

def PostFromSoup(soup, permalink):
	p = Post()
	p.content = u'\n'.join([unicode(x) for x in soup.find('div','post-body').contents]).strip()
	p.title = soup.find('h3','post-title').string
	p.author = soup.find('p','post-meta').a.string
	p.permalink = permalink

	permalinkParts = permalink.split('/')
	p.published = datetime(int(permalinkParts[3]),int(permalinkParts[4]),int(permalinkParts[5]))
	
	p.tags = [t.string for t in soup.findAll('a',rel='category tag')]
	return p
	
def CommentPageURLsFromSoup(soup, permalink):
	return [permalink]
	
def PermalinksFromSoup(soup):
	main = soup.find('div','sec-posts')
	titlesNodes = main.findAll('h3', 'post-title')
	if titlesNodes == None:
		return None
	titles = []
	for title in titlesNodes:
		titles.append(title.a['href'])
	return titles

def PageURLGenerator():
	pageNo = 0
	while True:
		pageNo = pageNo + 1
		yield "http://desipundit.com/page/" + str(pageNo)
