import lxml.html

def html2text(html):
    return unicode(lxml.html.fromstring(html).text_content())
