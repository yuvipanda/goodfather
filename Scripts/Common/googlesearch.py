import re
import locale
from urllib2 import urlopen, Request

reactionsCountRe = re.compile(r'of <b>(?P<count>(?:\d|,)+)</b>')
searchCountRe = re.compile(r'of about <b>(?P<count>(?:\d|,)+)</b>')
#I need to do this for parsing comma seperated numbers. Sucks, I know. 
#See here: http://mail.python.org/pipermail/python-list/2003-November/238093.html
locale.setlocale(locale.LC_NUMERIC, "English") 

def blog_reactions_count(url):
	searchUrl = "http://blogsearch.google.com/blogsearch?hl=en&ie=UTF-8&q=link:%s&filter=0" % url
	text = urlopen(searchUrl).read()
	results = re.findall(reactionsCountRe, text)
	if results:
		return locale.atoi(results[0])
	else:
		return 0

def search_results_count(url):
	searchUrl = "http://www.google.co.in/search?q=%s" % url
	req = Request(searchUrl, headers={'User-Agent':'GoodFather 0.9'})
	text = urlopen(req).read()
	results = re.findall(searchCountRe, text)
	if results:
		return locale.atoi(results[0])
	else:
		return 0

