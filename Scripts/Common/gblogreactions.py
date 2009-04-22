import re
import locale
from urllib2 import urlopen

countRe = re.compile(r'of <b>(?P<count>(?:\d|,)+)</b>')

#I need to do this for parsing comma seperated numbers. Sucks, I know. 
#See here: http://mail.python.org/pipermail/python-list/2003-November/238093.html
locale.setlocale(locale.LC_NUMERIC, "English") 

def reactions_count(url):
	searchUrl = "http://blogsearch.google.com/blogsearch?hl=en&ie=UTF-8&q=link:%s&filter=0" % url
	text = urlopen(searchUrl).read()
	result = re.findall(countRe, text)
	if result:
		return locale.atoi(re.findall(countRe, text)[0])
	else:
		return 0
