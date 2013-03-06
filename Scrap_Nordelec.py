'''Tool for downloading the information on the companies 
in the Nordelec building in the city of Montreal'''

import re
from lxml import etree
from lxml.cssselect import CSSSelector
from scraptools import getUrlContent

def printUnitIdInfo(unit_id):
    '''Prints all the info associated with the unit_id if any'''
    href = 'http://lenordelec.ca/modules/imdirectory/unit.php?unit_id=%d' % unit_id
    source = getUrlContent(href)
    html = etree.HTML(source)

    selTitle = CSSSelector('div.imdirectory_unit_container_info h1')
    title = selTitle(html)
    
    if len(title):  # Check if page has info
        print 'unit_ID\t{}'.format(unit_id)
        print 'Nom locataire\t{}'.format(title[0].text)
        selInfos = CSSSelector('div.unit_info')
        selTitle = CSSSelector('div.title')
        selValue = CSSSelector('div.value')
        infos = selInfos(html)
        
        # Iterate on all data fields
        for info in infos:
            title = selTitle(info)[0]
            value = selValue(info)[0]
            try:
                valueText = etree.tostring(value, method="text", with_tail=False)
                valueText = re.sub('[\t\r\n]', '', valueText).rstrip()
            except Exception as e:
                valueText = str(e)
                
            print  '{}\t{}'.format(title.text, valueText)
        print

if __name__ == '__main__':
    #Example to scrap every company
    for unit_id in xrange(300):
        printUnitIdInfo(unit_id)
