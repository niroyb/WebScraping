from urllib2 import urlopen
from os import path
from sys import stderr
from urllib import urlretrieve

# LXML : pypi.python.org/pypi/lxml
from lxml import etree
from lxml.cssselect import CSSSelector

def getElements(url, cssSelector):
    source = getUrlContent(url)
    html = etree.HTML(source)
    selector = CSSSelector(cssSelector)
    return selector(html)

def getUrlContent(url):
    '''Gets the content of a url as a string'''
    try:
        f = urlopen(url)
        s = f.read()
        f.close()
    except Exception as e:
        print >> stderr, e, url
        return None
    return s

def downloadRessource(url, destPath='', fileName=None):
    '''Saves the content at url in folder destPath as fileName''' 
    # Default filename
    if fileName == None:
        fileName = path.basename(url)
    
    # Add final backslash if missing
    if destPath != None and len(destPath) and destPath[-1] != '/':
        destPath += '/'
        
    urlretrieve(url, destPath + fileName)
