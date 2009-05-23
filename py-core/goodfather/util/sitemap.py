from urllib2 import urlopen 
from lxml import objectify
from dateutil import parser

class UrlEntry:
    def __init__(self, loc, changefreq, priority, lastmod):
        self.loc = loc
        self.changefreq = changefreq
        self.priority = priority
        self.lastmod = lastmod


def parse_sitemap(url):
    root = objectify.parse(urlopen(url)).getroot()

    for c in root.iterchildren():
        yield UrlEntry(loc = str(c.loc),
                       changefreq = str(c.changefreq), 
                       priority = float(c.priority), 
                       lastmod = parser.parse(str(c.lastmod)))
    

