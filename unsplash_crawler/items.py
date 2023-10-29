# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class UnsplashCrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    url = scrapy.Field()
    tags = scrapy.Field()
    download_path = scrapy.Field()
