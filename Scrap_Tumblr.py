import re
from scraptools import getElementsFromUrl, downloadResource

def getImgSrcs(url):
    '''returns the src attribute of all images on a page'''
    elems = getElementsFromUrl(url, 'img')
    imgSrcs = [e.get('src') for e in elems]
    return imgSrcs

def cleanImgSrcs(imgSrcs):
    '''Returns the src of images that are not avatars or ads'''
    clean = [src for src in imgSrcs if 'avatar' not in src and
             re.search('//\d\d?', src)]
    return clean
    
def getSearchImgs(query, limit=None):
    '''Gets the src of images on tumblr tagged with query'''
    query = query.replace(' ', '%20')
    searchPage = 'http://www.tumblr.com/tagged/' + query
    
    elems = getElementsFromUrl(searchPage, 'a.go')
    
    postUrls = [e.get('href') for e in elems]
    if limit is None or limit > len(postUrls):
        limit = len(postUrls)
    #print postUrls
    imageSrcs = []
    for i, postUrl in enumerate(postUrls[:limit], 1):
        print i, '/', limit, postUrl
        
        #Find pictures directly on post
        newSrcs = cleanImgSrcs(getImgSrcs(postUrl))
        print '\tFound :', len(newSrcs)
        imageSrcs += newSrcs
        
        #Find pictures in post iframe
        elems = getElementsFromUrl(postUrl, 'iframe.photoset')
        iframeUrls = [e.get('src') for e in elems]
        for iframeUrl in iframeUrls:
            print '\tiframe:', iframeUrl
            iframeImageSrcs = cleanImgSrcs(getImgSrcs(iframeUrl))
            print '\tFound :', len(iframeImageSrcs)
            imageSrcs += iframeImageSrcs

    return imageSrcs

if __name__ == '__main__':
    print 'Getting image srcs...'
    srcs = getSearchImgs('cat')
    
    print 'Result:'
    print '\n'.join(srcs)
    
    print 'Downloading images...'
    for i, src in enumerate(srcs, 1):
        print i, '/', len(srcs)
        downloadResource(src, destPath='tumblr')
