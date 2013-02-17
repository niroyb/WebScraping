'''Shows all masculin first names from french website'''

from scraptools import getElements

for pageNb in xrange(1,40):
    href = 'http://www.quelprenom.com/prenom-garcon.php?page=%d'%pageNb
    for nameTag in getElements(href, '.prenom-lien'):
        print nameTag.text