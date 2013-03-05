'''Prints the titles of RSS feeds'''

import feedparser
#http://pypi.python.org/pypi/feedparser/
#pip install feedparser

def getArticleTitles(rssHref):
    '''Returns a list of the titles from the given rssFeed'''
    feed = feedparser.parse(rssHref)
    titles = [entry.title for entry in feed.entries]
    return titles


if __name__ == '__main__':
    rssHrefs = ['http://feeds.gawker.com/gizmodo/excerpts.xml',
             'http://rss.cbc.ca/lineup/topstories.xml',
             'http://feeds.reuters.com/reuters/topNews']
    
    for rssHref in rssHrefs:
        print rssHref
        titles =  getArticleTitles(rssHref)
        print '\n'.join(titles)
        print