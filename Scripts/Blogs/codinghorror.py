from goodfather import gfpersist
from lxml import html
from urllib2 import urlopen
from dateutil import parser
import pdb

class Blog(gfpersist.PersistanceContainer):
    pass

class Post(gfpersist.Persistable):
    pass

class Comment(gfpersist.Persistable):
    pass

def comment_from_node(node):
    node = html.fromstring(html.tostring(node, encoding='UTF-8'))
    comment = Comment()
    meta = node[-1]
    authorLink = meta.find('a')
    if authorLink is not None:
        comment.AuthorLink = authorLink.get('href')
        comment.Author = authorLink.text
    else:
        comment.Author = meta.text_content().split(' on ')[0].strip()

    try:
        comment.PostedAt = parser.parse(meta.text_content().split(' on ')[-1])
    except:
        pdb.set_trace()

    node.remove(node[-1])

    comment.Contents = html.tostring(node)

    return comment


def post_from_page(url):
    post = Post()
    doc = html.parse(urlopen(url)).getroot()
    post.Title = doc.find_class('title-link')[0].text
    post.Permalink = doc.find_class('title-link')[0].get('href')

    post.PostedAt = parser.parse(doc.find_class('date')[0].text)
    
    content = doc.find_class('blogbody')[0]

    # Remove the 'breadcrumb' navigator, postedtime & title
    crumbnode = content[-1]
    postednode = content[-2]
    titlenode = content[0]

    if titlenode.tag == 'h3' and titlenode.attrib['class'] == 'blogbody':
        content.remove(titlenode)

    if crumbnode.tag == 'div':
        content.remove(crumbnode)

    if postednode.tag == 'div' and postednode.get('class') == 'posted':
        content.remove(postednode)

    post.Contents = html.tostring(content)

    post.Comments = []

    # Last node with class 'comments-body' is comment form
    commentNodes = doc.find_class('comments-body')[:-1] 

    for commentNode in commentNodes:
        post.Comments.append(comment_from_node(commentNode))
    
    return post

def get_permalinks(url):
    doc = html.parse(urlopen(url))
    permalinks = doc.xpath("//div[@class='blogbody']//a")
    for p in permalinks:
        yield p.get('href')

if __name__ == "__main__":
    blog = Blog(filepath="codinghorror.blog", createnew=False)
    for ui in get_permalinks("http://codinghorror.com/blog/archives.html"):
        if not blog.has_key(ui):
            p = post_from_page(ui)
            blog.persist(p.Permalink, p)
            print "Done %s, %s comments" % (ui, len(p.Comments))
        else:
            print "Skipped %s" % ui
             

