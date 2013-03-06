import feedparser
import re

def getRssOfSubReddit(subreddit):
    '''Returns the url of the rss page of a subreddit'''
    return 'http://www.reddit.com/r/{}/.rss'.format(subreddit)

class RedditPost():
    '''Object containing info from a post'''
    def __init__(self, rssEntry):
        '''Init with a feedparser entry object'''
        self.title = rssEntry.title_detail['value']
        self.linkPost = rssEntry.link
        html = rssEntry.summary_detail['value'].encode('ascii', 'ignore')
        #prettyPrint(html)

        self.submittedBy = re.search('submitted by <.*?> (.*?) <', html).group(1)
        self.subreddit = re.search('to <.*?> (.*?)<', html).group(1)
        self.linkOut = re.search('href="([^\s]+)">\[link\]', html).group(1)
    
    def __str__(self):
        return str(self.__dict__)

if __name__ == '__main__':
    feed = feedparser.parse(getRssOfSubReddit('all'))
    posts = [RedditPost(entry) for entry in feed.entries]
    
    for post in posts:
        print post
                  
              
