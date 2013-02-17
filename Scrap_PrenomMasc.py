'''Shows all masculin first names from french website'''

from scraptools import getElements, urlIterator

startUrl = 'http://www.quelprenom.com/prenom-garcon.php'
nextCssSelector = 'span.button-right'

for href in urlIterator(startUrl, nextCssSelector):
    for nameTag in getElements(href, '.prenom-lien'):
        print nameTag.text