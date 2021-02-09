# Hashtag Basketball scraping
Script to scrape player projections data from Hashtag Basketball and rank them based on stats.

Gets player projections from [Hashtag Basketball]('https://hashtagbasketball.com/fantasy-basketball-projections') and extract the stats in my ESPN points league game. The script outputs a CSV with the players' stats, total points based on the given `scoring` dictionary and ranks players by points.


The `scoring` dictionary contains the weights of each stat in my league - change as necessary.

The Hashtag Basketball website uses AJAX to update the page when you set different weights or check/uncheck categories. While it is possible to use the `requests` module to do this by intercepting the AJAX call and reproducing it as the request, it is probably easier to use something more robust such as [Scrapy](https://scrapy.org/) or [Selenium](https://pypi.org/project/selenium/). All the data I needed was present in the default page, so I didn't need to use this.
