WebScraping Tools
=================

This repo contains examples of web scraping.
Dependencies are [lxml](http://pypi.python.org/pypi/lxml) for DOM traversal and [feedparser](http://pypi.python.org/pypi/feedparser) for RSS.

There is also a utility class "scraptools" to group common scraping operations:
* getDOM : Returns the DOM element of the page for the given url
* getElementsFromHTML : Returns a list of lxml elements from html source corresponding to a cssSelector
* getElementsFromUrl : Returns a list of lxml elements from the page fetched at url corresponding to a cssSelector
* getUrlContent : Gets the content of a url as a string
* downloadResource : Download the content of a  url to the disk
* saveResource : Saves data to file in binary write mode
* urlIterator : Successively yields page urls while there is a next one found by the cssSelector

Examples:
--------
* Scrap_Eduportefolio : Get names of students attending Polytechnique Montreal
* Scrap_GoogleImg : Download top imgages for a search on Google image
* Scrap_Imgur : Download individual images or a whole gallery
* Scrap_Moodle : Recursively downloads all the files from the course pages on Moodle
* Scrap_Nordelec : Get information about the companies inside this building
* Scrap_PrenomMasc : Get first names from a website
* Scrap_Reddit : Parses posts from a subreddit
* Scrap_RSS_titles : Get the article titles of rss feeds. Usefull for a quick glance at the news from the console ;)
* Scrap_Tumblr : Gets pictures based on their tags