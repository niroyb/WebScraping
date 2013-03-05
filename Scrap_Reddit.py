

import feedparser
import scraptools

def getRssOfSubReddit(subreddit):
    return 'http://www.reddit.com/r/{}/.rss'.format(subreddit)

class RedditPost():
    def __init__(self, rssEntry):
        self.title = rssEntry.title_detail['value']
        self.linkPost = rssEntry.link
        html = rssEntry.summary_detail['value']
        links = scraptools.getElementsFromHTML(html, 'a')
        self.submittedBy = links[1].text
        self.subreddit = links[2].text
        self.linkOut = links[3].get('href')
    
    def __str__(self):
        #for key in self.__dict__.keys():
        #    print key, self.__dict__[key]
        #print self.__dict__
        return '\n'.join(str(s) for s in self.__dict__.items())
        
        #attribs = [self.title, self.linkPost, self.submittedBy,
        #           self.subreddit, self.]

feed = feedparser.parse(getRssOfSubReddit('all'))
posts = [RedditPost(entry) for entry in feed.entries]

for post in posts:
    print str(post)

#print '\n'.join(posts)
              
              
