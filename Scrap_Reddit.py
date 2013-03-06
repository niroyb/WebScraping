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

        self.submittedBy = re.search('submitted by <.*?> (.*?) <', html).group(1)
        self.linkOut = re.search('href="([^\s]+)">\[link\]', html).group(1)
        subredditGroup = re.search('to <.*?> (.*?)<', html)
        if subredditGroup: #Subreddit found in html of description
            self.subreddit = subredditGroup.group(1)
        else: #Extract subreddit from post url
            self.subreddit = re.search('/r/(.*?)/', self.linkPost).group(1)
    
    def __str__(self):
        return str(self.__dict__)

if __name__ == '__main__':
    # Parse rss feed
    feed = feedparser.parse(getRssOfSubReddit('all'))
    # Generate posts for every feed item
    posts = [RedditPost(entry) for entry in feed.entries]
    # Print all posts informations
    for post in posts:
        print post