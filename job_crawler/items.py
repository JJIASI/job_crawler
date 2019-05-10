# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class JobCrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    jobsalary = scrapy.Field()
    jobname = scrapy.Field()
    jobcompany = scrapy.Field()
    jobexp = scrapy.Field()
    jobedu = scrapy.Field()
    jobarea = scrapy.Field()
    jobindcat = scrapy.Field()
    jobdate = scrapy.Field()
    jobapply = scrapy.Field()
    sourceweb = scrapy.Field()
    keyword = scrapy.Field()
#     pass
