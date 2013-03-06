'''Shows all masculin first names from french website'''

from scraptools import getElementsFromUrl, urlIterator

startUrl = 'http://www.quelprenom.com/prenom-garcon.php'
nextCssSelector = 'span.button-right'

#Iterate on all the pages successively
for href in urlIterator(startUrl, nextCssSelector):
    #Iterate on all the names of a page
    for nameTag in getElementsFromUrl(href, '.prenom-lien'):
        print nameTag.text