'''Tool for scraping images from the website Imgur'''
import urllib2
import re

from scraptools import downloadRessource, getElementsFromUrl

def getImgurGalleryHrefTitle(galleryAddress):
    '''Returns tuples of page href and img title
    href points to the page containing the image(s) not the actual image'''
    
    ret = []
    for e in getElementsFromUrl(galleryAddress, 'div.post > a'):
        src = urllib2.urlparse.urljoin(galleryAddress, e.get('href'))
        imgTag = e.find('img')
        title = imgTag.get('title')
        title = re.sub('<p>.+?</p>', '', title)  # Remove nbr of views
        ret.append((src, title))
    return ret

def getImgurImageSrcs(href):
    '''Returns a list of the src parametre of the image(s) from the page'''
    ret = []
    for e in getElementsFromUrl(href, 'div#image img'):
        src = e.get('src')
        src = re.sub('\?.*', '', src)  # remove trailing parameters
        ret.append(src)
    return ret

def downloadImgurPage(href, destPath=''):
    '''Downloads all the images from an imgur page or album'''
    imgSrcs = getImgurImageSrcs(href)
    for src in imgSrcs:
        downloadRessource(src, destPath)
    
def downloadImgurGallery(galleryAddress, destPath=''):
    '''Downloads all the images linked on a gallery'''
    HrefTitles = getImgurGalleryHrefTitle(galleryAddress)
    for href, title in HrefTitles:
        downloadImgurPage(href)

# Examples:
downloadImgurPage('http://imgur.com/gallery/O87xG')
# downloadImgurGallery('http://imgur.com/r/aww', 'Imgur/')
# downloadImgurGallery('http://imgur.com/', 'Imgur/')
