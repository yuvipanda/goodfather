import lxml.html

def html2text(html):
	return lxml.html.fromstring(html).text_content()
