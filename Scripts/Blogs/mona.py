from goodfather import gfpersist
from goodfather.util import sitemap
from lxml import html
from urllib2 import urlopen

class Blog(gfpersist.PersistanceContainer):
    pass

class Post(gfpersist.Persistable):
    pass

class Comment(gfpersist.Persistable):
    pass

def post_from_page(url):
    post = Post()
    doc = html.parse(urlopen(url)).getroot()
    post.Title = doc.find_rel_links('bookmark')[0].text
    post.Permalink = doc.find_rel_links('bookmark')[0].get('href')
    
    meta = doc.find_class('metadata')[0]
    tags = meta.find_rel_links('tag')
    if tags:
        post.Tags = [t.text for t in tags]

    categories = meta.find_rel_links('category tag')
    if categories:
        post.Categories = [c.text for c in categories]

    snap_preview = doc.find_class('snap_preview')[0]
    post.Contents = html.tostring(snap_preview)
    
#    commentstring = doc.get_element_by_id('comments').text.split()[0]
#    if commentstring == "No":
#        post.Comments = 0
#    else:
#        post.Comments = int(commentstring)
    return post

if __name__ == "__main__":
    blog = Blog(filepath="mona.blog", createnew=False)
    for ui in sitemap.parse_sitemap("http://pixelbits.wordpress.com/sitemap.xml"):
        if not '/20' in ui.loc:
            #guards against non-post pages. Needs to be more robust
            #But okay for now!
            continue
            
        if not blog.has_key(ui.loc):
            p = post_from_page(ui.loc)
            p.PostedAt = ui.lastmod
            blog.persist(ui.loc, p)
            print "Done %s" % ui.loc
        else:
            print "Skipped %s" % ui.loc
             

