WebScraping Tools
=================

This repo contains examples of web scraping using lxml and feedparser
lxml : 
feedparser :

There is also a utility class "scraptools" to group common scraping operations:
* getElements : Get lxml elements corresponding to a cssSelector
* getUrlContent : Gets the content of a url as a string
* downloadRessource : Download the content of a  url to the disk

Examples:
--------
* Scrap_Imgur : Download individual images or a whole gallery
* Scrap_Nordelec : Get information about the companies inside this building
* Scrap_Eduportefolio : Get names of students attending Polytechnique Montreal
* Scrap_PrenomMasc : Get first names from a website
* Scrap_RSS_titles : Get the article titles of rss feeds. Usefull for a quick glance at the news from the console ;)