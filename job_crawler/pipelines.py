# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from pymongo import MongoClient
from scrapy.exceptions import DropItem

class JobCrawlerPipeline(object):
    def process_item(self, item, spider):
        return item

class DuplicatesPipeline(object):
    '''Avoid Data Deduplication
    Take jobname and jobcompany to find duplicate data.
    
    '''    
    def __init__(self):
        self.job_data = set()
    def process_item(self, item, spider):
        job_name = item['jobname'] 
        job_company = item['jobcompany']
        if (job_name in self.job_data) and ((job_company in self.job_data)):
            raise DropItem('duplicates data found %s', item)
        self.job_data.add(job_name)
        return(item)

class MongoDBPipline(object):
    '''Write data to database
    
    '''
    def open_spider(self, spider):
        db_uri = spider.settings.get('MONGODB_URI', 'mongodb://localhost:27017')
        db_name = spider.settings.get('MONGO_DB_NAME', 'job_data')
        self.db_client = MongoClient('mongodb://localhost:27017')
        self.db = self.db_client[db_name]
        
    def close_spider(self, spider):
        self.db_client.close()
        
    def process_item(self, item, spider):
        self.insert_db(item)
        
        return item
    
    def insert_db(self, item):
        item = dict(item)
        self.db.job_data.insert_one(item)
        
        
        