# -*- coding: utf-8 -*-
import scrapy


class SecScrapeItem(scrapy.Item):
    file_urls = scrapy.Field()
    files = scrapy.Field()
    myFile = scrapy.Field()
    company = scrapy.Field()
    directory = scrapy.Field()

