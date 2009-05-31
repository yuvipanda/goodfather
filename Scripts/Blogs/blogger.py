import sys

from lxml import html
from urllib2 import urlopen
from dateutil import parser

from gdata import service

from goodfather import gfpersist

class Post(gfpersist.Persistable):
    pass

class Comment(gfpersist.Persistable):
    pass

class Blog(gfpersist.PersistanceContainer):
    pass

def get_service_url(url):
    page = html.parse(urlopen(url))
    return page.find("//link[@rel='service.post']").get('href')

def entry_to_post(entry):
    p = Post()
    p.Title = entry.title.text
    p.Contents = entry.content.text
    p.PostedAt = parser.parse(entry.published.text)
    p.Categories = [ c.term for c in entry.category ]
    p.Author = e.author[0].name.text
    p.Permalink = e.GetHtmlLink().href 
    return p

def entry_to_comment(entry):
    c = Comment()
    c.Contents = entry.content.text
    c.PostedAt = parser.parse(entry.published.text)
    c.Author = entry.author[0].name.text
    if entry.author[0].uri:
        c.AuthorUrl = entry.author[0].uri.text
    return c

if __name__ == '__main__':
    limit = sys.argv[1]
    blogurl = sys.argv[2]
    filename = sys.argv[3]

    get_comments = not ('-nc' in sys.argv)

    blog = Blog(filename)

    count = 0
    
    serv = service.GDataService()
    postsQ = service.Query()
    postsQ.feed = get_service_url(blogurl)
    postsQ.max_results = limit

    feed = serv.Get(postsQ.ToUri())    

    # I should probably use a regex for this, but hey!
    blog_id = feed.id.text.split(':')[-1].split('-')[-1]

    for e in feed.entry:
        p = entry_to_post(e)
        if blog.has_key(p.Permalink):
            continue
        if get_comments:
            post_id = e.id.text.split('-')[-1]

            p.Comments = []
            commentsUri = 'http://www.blogger.com/feeds/%s/%s/comments/default' % (blog_id, post_id)
            commentsFeed = serv.Get(commentsUri)        
            for c in commentsFeed.entry:
                p.Comments.append(entry_to_comment(c))

        blog.persist(p.Permalink, p)
        print "Done %s, at %s" % (p.Title, p.PostedAt)





