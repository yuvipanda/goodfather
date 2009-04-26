from goodfather import gfpersist
from goodfather.util import googlesearch
from BeautifulSoup import BeautifulSoup
from urllib2 import urlopen
import sys

class Tag (gfpersist.Persistable):
	pass

class SOTags (gfpersist.PersistanceContainer):
	pass

def tags_from_page(page):
	tagNodes = page.findAll('a', rel='tag')
	tags = []
	for t in tagNodes:
		tag = Tag()
		tag.Name = t.string
		tag.Questions = int(t.nextSibling.string.split(';')[-1])
		tag.BlogMentions = googlesearch.blog_mentions_count(tag.Name)
		tag.SearchResultsCount = googlesearch.search_results_count(tag.Name)
		tags.append(tag)
	return tags

def soup_for_pagenumber(pageNo):
	url = "http://stackoverflow.com/tags?page=%s" % pageNo
	return BeautifulSoup(urlopen(url).read())

if __name__ == '__main__':
	filename = sys.argv[1]
	allTags = SOTags(filename)

	#figure out last page
	firstPage = soup_for_pagenumber(1)
	lastPage = int(firstPage.findAll('span','page-numbers')[-1].string)
	for i in xrange(1, lastPage + 1):
		tags = tags_from_page(soup_for_pagenumber(i))
		for t in tags:
			allTags.persist(t)
			print "Done: ", t.Name
	
