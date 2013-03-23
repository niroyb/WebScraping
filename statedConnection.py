'''Utility functions to deal with connections requiring logins and cookies'''

import cookielib
import urllib
import urllib2

def getSateConnection(loginUrl, valueDict, headers = None):
    '''Returns the response and statedOpener for login Url with data'''
    #the opener maintains cookies
    cookies = cookielib.CookieJar()

    opener = urllib2.build_opener(
        urllib2.HTTPRedirectHandler(),
        urllib2.HTTPHandler(debuglevel=0),
        urllib2.HTTPSHandler(debuglevel=0),
        urllib2.HTTPCookieProcessor(cookies))
    
    if isinstance(headers, list):
        opener.addheaders = headers

    data = urllib.urlencode(valueDict)
    response = opener.open(loginUrl, data)

    return response, opener

def parseResponse(response):
    '''Returns the httpHeaders and the content of the response'''
    http_headers = response.info()
    the_page = response.read()
    return http_headers, the_page



