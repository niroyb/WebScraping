'''Aggregates 97 good programming practices and generates a printer friendly html page'''

import scraptools
from urllib2 import urlparse
from lxml import etree

head = '''<html>
<head>
<style TYPE="text/css">
body, p, div, li, td { font-family:Verdana,Arial,Helvetica,sans-serif; color:#222222; font-size:11px; }
h1 {page-break-before: always;}
</style>
</head>
<body>
'''

def getHTMLContent(url):
    '''Get html code of main content of a url on Oreilly'''
    elems = scraptools.getElementsFromUrl(url, '#content')
    content = elems[0]
    return etree.tostring(content, pretty_print=True, method="html")
    

def scrapOreily(indexUrl, outName):
    '''Generates an html page from the index located at indexUrl'''
    links = scraptools.getElementsFromUrl(url, '#bodyContent ol a:nth-child(1)')
    
    f = open(outName, 'w')
    
    f.write(head)
    
    f.write(getHTMLContent(indexUrl))
    
    for link in links:
        relativeLink = link.get('href')
        print relativeLink
        absoluteLink = urlparse.urljoin(url, relativeLink)
        
        f.write(getHTMLContent(absoluteLink))
        
    f.write('</body></html>')
    f.close()

url = ('http://programmer.97things.oreilly.com/wiki/index.php/'
       'Contributions_Appearing_in_the_Book')

scrapOreily(url, '97 things a programmer should know.html')