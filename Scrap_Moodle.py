# -*- coding: cp1252 -*-
'''Scrap_Moodle.py : Recursively downloads all the files from 
the course pages on Moodle'''

'''
Written in Python 2.7.3
Dependencies :
    lxml (pypi.python.org/pypi/lxml)
    statedConnection and scraptools from https://github.com/niroyb/WebScraping
'''

__author__ = "Nicolas Roy"
__date__ = "2013-03-23"
__version__ = "1.0"

import scraptools
from lxml.cssselect import CSSSelector
from statedConnection import getSateConnection
import re
from os.path import basename
from sys import stderr
import getpass

class MoodleConnect:
    '''Moodle connection object with credentials'''
    def __init__(self, loginUrl, username, password):
        valueDict = {'username' : username, 'password' : password}

        # Change User agent
        headers = [('User-agent', 'pyMoodleCrawler/1.0')]
        response, self.opener = getSateConnection(loginUrl, valueDict, headers)

        self.main_page = response.read()
    
    def getUrlData(self, url):
        '''Returns data at url, can be a file or a page html'''
        response = self.opener.open(url)
        page = response.read()
        return page

class Resource():
    '''Represents an element to download'''
    def __init__(self, url, instanceName = ''):
        self.url = url #url ending with resource id
        self.instanceName = instanceName
    
    @staticmethod
    def getResourceUrl(source):
        '''Returns the resource url from the resourceWorkaroundPageSource'''
        elems = scraptools.getElementsFromHTML(source, '.resourceworkaround>a')
        if len(elems) == 0:  # The resource is probably embedded in the page
            container = scraptools.getElementsFromHTML(source, 'object')
            if len(container) == 0:  # Some other type of container
                container = scraptools.getElementsFromHTML(source, 'frame')
                href = container[1].get('src')
            else:
                href = container[0].get('data')
        else:
            href = elems[0].get('href')
        return href
     
    def saveTo(self, path):
        response = connection.opener.open(self.url)
        http_headers = response.info()
        data = response.read()
        
        if 'content-disposition' in http_headers.keys():
            # The server is answering with a file
            cd = http_headers['content-disposition']
            fName = re.search('filename="(.*)"', cd).group(1)
        else:
            # We got a workaround page, Extract real resource url
            resourceUrl = Resource.getResourceUrl(data)
            fName = basename(resourceUrl)  # Get resource name
            data = connection.getUrlData(resourceUrl)  # Get resource
        
        print 'Saving ', fName
        scraptools.saveResource(data, fName, path)  # Save file

class ResourceFolder():
    def __init__(self, connection, url, folderName):
        self.connection = connection
        self.url = url
        self.folderName = folderName
        self.resources = []
    
    def extractResources(self):
        pageSource = connection.getUrlData(self.url)
        resourceElems = scraptools.getElementsFromHTML(pageSource, '#region-main a')
        print len(resourceElems), 'files found in folder', self.folderName
        
        for a in resourceElems:
            self.resources.append(Resource(a.get('href'), a.text))
    
    def saveTo(self, path):
        if len(self.resources) == 0:
            self.extractResources()
        
        path = scraptools.checkPath(path)
        for r in self.resources:
            r.saveTo(path + self.folderName) #Save in subfolder

class MoodleCoursePage():
    def __init__(self, connection, pageUrl, sigle):
        self.moodleConnection = connection
        self.pageUrl = pageUrl
        self.sigle = sigle
        self.resources = []
    
    @staticmethod
    def getUrlAndInstanceName(element): #could be split in 2 functions
        selector = CSSSelector('.instancename')
        nameSpan = selector(element)[0]
        instanceName = nameSpan.text
        
        selector = CSSSelector('a')
        aTag = selector(element)[0]
        href = aTag.get('href')
        
        return href, instanceName
    
    def extractResources(self):
        '''Extracts the resources from a course page'''
        pageSource = connection.getUrlData(self.pageUrl)
        resourceElems = scraptools.getElementsFromHTML(pageSource, '.resource')
        print len(resourceElems), 'Direct resources found'
        
        self.resources = []
        for element in resourceElems:
            url, instanceName = self.getUrlAndInstanceName(element)
            self.resources.append(Resource(url, instanceName))
            
        # Look for folders
        folderElems = scraptools.getElementsFromHTML(pageSource, '.folder')
        print len(folderElems), 'Folders found'
        for folder in folderElems:
            url, instanceName = self.getUrlAndInstanceName(folder)
            self.resources.append(ResourceFolder(connection, url, instanceName))

    def saveResources(self):
        if len(self.resources) == 0:
            self.extractResources()
            
        for r in self.resources:
            try:
                r.saveTo(self.sigle)
            except Exception as e:
                print >> stderr, e, self.pageUrl

class MoodleMyPage():
    def __init__(self, moodleConnection):
        
        pageSource = moodleConnection.main_page
        
        # Find course boxes
        elems = scraptools.getElementsFromHTML(pageSource, '.course_title a')
        
        genieRe = '[A-Z]{1,4}-?([A-Z]{3})?'
        numRe = '[0-9]{3,4}[A-Z]?'
        sigleRe = '(' + genieRe + numRe + ')'
        
        self.coursePages = []
        for e in elems:
            courseDescription = e.text
            match = re.match(sigleRe, courseDescription)
            if match: #We have a course box with a valid sigle
                sigle = match.group(1)
                pageUrl = e.get('href')
                self.coursePages.append(MoodleCoursePage(moodleConnection, pageUrl, sigle))
        
    def downloadDocuments(self):
        for course in self.coursePages:
            print 'Downloading documents for course', course.sigle
            course.saveResources()  
            print

def test_mypage(mypage):
    assert len(myPage.coursePages) > 0, "Error no courses found"
    #print '\n'.join([c.sigle  for c in myPage.coursePages])
    #print connection.main_page
    #print '\n'.join([c.sigle  for c in myPage.coursePages])

if __name__ == '__main__':
    
    loginUrl = 'https://moodle.polymtl.ca/login/index.php'
    print 'Credentials', loginUrl
    username = raw_input('username: ')
    password = getpass.getpass('password: ')
    
    #username, password = open('moodleCredentials.txt').read().splitlines()
    print 'Establishing Connection...'
    connection = MoodleConnect(loginUrl, username, password)
    myPage = MoodleMyPage(connection)
    test_mypage(myPage)
    myPage.downloadDocuments()
