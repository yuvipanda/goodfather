import re
import locale
from urllib2 import urlopen, Request

countRe = re.compile(r'of (?:about )?<b>(?P<count>(?:\d|,)+)</b>')
searchCountRe = re.compile(r'of about <b>(?P<count>(?:\d|,)+)</b>')
#I need to do this for parsing comma seperated numbers. Sucks, I know. 
#See here: http://mail.python.org/pipermail/python-list/2003-November/238093.html
locale.setlocale(locale.LC_NUMERIC, "English") 

def _count_results(url):
	req = Request(url, headers={'User-Agent':'GoodFather 0.9'})
	text = urlopen(req).read()
	results = re.findall(countRe, text)
	if results:
		return locale.atoi(results[0])
	else:
		return 0

def blog_mentions_count(terms):
	searchUrl = "http://blogsearch.google.com/blogsearch?hl=en&ie=UTF-8&q=%s&filter=0" % terms
	return _count_results(searchUrl)

def blog_reactions_count(url):
	return blog_mentions_count('link:%s' %url) 

def search_results_count(terms):
	searchUrl = "http://www.google.co.in/search?q=%s" % terms
	return _count_results(searchUrl)
