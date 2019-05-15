# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class JobCrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    jobsalary = scrapy.Field() # 薪資
    jobname = scrapy.Field()   # 職稱
    jobcompany = scrapy.Field()# 公司名稱
    jobexp = scrapy.Field()    # 經驗條件
    jobedu = scrapy.Field()    # 學歷條件
    jobarea = scrapy.Field()   # 工作地點
    jobindcat = scrapy.Field() # 產業
    jobdate = scrapy.Field()   # 更新日期
    jobapply = scrapy.Field()  # 應徵人數
    sourceweb = scrapy.Field() # 來源網站
    keyword = scrapy.Field()   # 關鍵字
#     pass
