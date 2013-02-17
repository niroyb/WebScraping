'''Utilities for scraping data from the internet'''

from urllib2 import urlopen, urlparse
from os import path
from sys import stderr
from urllib import urlretrieve

# LXML : pypi.python.org/pypi/lxml
from lxml import etree
from lxml.cssselect import CSSSelector

def getElements(url, cssSelector):
    '''Returns a list of lxml elements from url corresponding to the cssSelector'''
    source = getUrlContent(url)
    html = etree.HTML(source)
    selector = CSSSelector(cssSelector)
    return selector(html)

def urlIterator(startUrl, nextCssSelector):
    '''Yields the url of a page while there is a next one found by the cssSelector'''
    #This function takes time because it has to parse the dom to get the next url
    url = startUrl
    while url:
        yield url
        nextTags = getElements(url, nextCssSelector)
        url = None

        for possibleNext in nextTags:
            if possibleNext.tag == 'a':
                href = possibleNext.get('href')
                # Absolute href
                url = urlparse.urljoin(startUrl, href)
                break
            else:
                newTag = possibleNext.find('a')
                if newTag != None:
                    href = newTag.get('href')
                    url = urlparse.urljoin(startUrl, href)
                    break

def prettyPrint(element):
    '''Factory function to pretty print an lxml element (for debugging)'''
    print etree.tostring(element, pretty_print=True, method="html")
        

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
