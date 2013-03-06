WebScraping Tools
=================

This repo contains examples of web scraping.
Dependencies are [lxml](http://pypi.python.org/pypi/lxml) for DOM traversal and [feedparser](http://pypi.python.org/pypi/feedparser) for RSS.

There is also a utility class "scraptools" to group common scraping operations:
* getElements : Get lxml elements corresponding to a cssSelector
* getUrlContent : Gets the content of a url as a string
* downloadRessource : Download the content of a  url to the disk
* urlIterator : Successively yields page urls while there is a next one found by the cssSelector 

Examples:
--------
* Scrap_Imgur : Download individual images or a whole gallery
* Scrap_GoogleImg : Download top imgages for a search on Google image
* Scrap_Nordelec : Get information about the companies inside this building
* Scrap_Eduportefolio : Get names of students attending Polytechnique Montreal
* Scrap_PrenomMasc : Get first names from a website
* Scrap_Reddit : Parses posts from a subreddit
* Scrap_RSS_titles : Get the article titles of rss feeds. Usefull for a quick glance at the news from the console ;)
* Scrap_Tumblr : Gets pictures based on their tags