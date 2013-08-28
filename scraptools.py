'''Utilities for scraping data from the internet'''

from urllib2 import urlopen, urlparse
from os import path, mkdir
from sys import stderr
from urllib import urlretrieve

# LXML : pypi.python.org/pypi/lxml
from lxml import etree
from lxml.cssselect import CSSSelector

def getDOM(url):
    '''Returns the DOM element of the page at url'''
    source = getUrlContent(url)
    DOM = etree.HTML(source)
    return DOM

def getElementsFromHTML(source, cssSelector):
    '''Returns a list of lxml elements from html source corresponding to the cssSelector'''
    dom = etree.HTML(source)
    selector = CSSSelector(cssSelector)
    return selector(dom)

def getElementsFromUrl(url, cssSelector):
    '''Returns a list of lxml elements from url corresponding to the cssSelector'''
    source = getUrlContent(url)
    return getElementsFromHTML(source, cssSelector)

def urlIterator(startUrl, nextCssSelector):
    '''Yields the url of a page while there is a next one found by the cssSelector'''
    #This function takes time because it has to parse the dom to get the next url
    url = startUrl
    while url:
        yield url
        nextTags = getElementsFromUrl(url, nextCssSelector)
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

def domIterator(startUrl, nextCssSelector):
    dom = getDOM(startUrl)
    nextSelector = CSSSelector(nextCssSelector)
    while dom is not None:
        yield dom
        nextTags = nextSelector(dom)
        dom = None
        for possibleNext in nextTags:
            if possibleNext.tag == 'a':
                url = possibleNext.get('href')
                url = urlparse.urljoin(startUrl, url)
                dom = getDOM(url)
                break

def prettyPrint(element):
    '''Factory function to pretty print an lxml element or html str (for debugging)'''
    if isinstance(element, str):
        element = element.replace('><','>\n<')
        element = etree.HTML(element)
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

def checkPath(destPath):
    # Add final backslash if missing
    if destPath != None and len(destPath) and destPath[-1] != '/':
        destPath += '/'
    
    if destPath != '' and not path.exists(destPath): 
        mkdir(destPath)
    return destPath

def saveResource(data, fileName, destPath=''):
    '''Saves data to file in binary write mode'''
    destPath = checkPath(destPath)
    with open(destPath + fileName, 'wb') as fOut:
        fOut.write(data)

def downloadResource(url, fileName=None, destPath=''):
    '''Saves the content at url in folder destPath as fileName''' 
    # Default filename
    if fileName == None:
        fileName = path.basename(url)
    
    destPath = checkPath(destPath)

    try:
        urlretrieve(url, destPath + fileName)
    except Exception as inst:
        print 'Error retrieving', url 
        print type(inst)     # the exception instance
        print inst.args      # arguments stored in .args
        print inst
    
