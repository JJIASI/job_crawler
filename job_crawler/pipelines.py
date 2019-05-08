# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from pymongo import MongoClient
from scrapy.exceptions import DropItem
import datetime

class JobCrawlerPipeline(object):
    def process_item(self, item, spider):
        return item

class JobItemPipeline(object):
    def process_item(self, item, spider):
        # jobdate
        if item['sourceweb'] == '1111人力銀行':
            item['jobdate'] = datetime.datetime.strptime(item['jobdate'], "%Y-%m-%d")
        elif item['sourceweb'] == '104人力銀行':
            item['jobdate'] = datetime.datetime.strptime('2019/'+item['jobdate'], "%Y/%m/%d")
        
        # jobexp
        if item['jobexp'] == '經驗不拘':
            item['jobexp'] = 0
        elif len(item['jobexp']) == 8:
            item['jobexp'] = int(item['jobexp'][0])
        elif len(item['jobexp']) == 9:
            item['jobexp'] = int(item['jobexp'][0:1])
        
        # jobsalay
        def salary_mean(salary,pay_form):
            if '~' in salary:
                s = salary.split(pay_form)[1].split('元')[0].split('~')
                func_t = lambda x:int(x.strip().replace(',',''))
                return int((func_t(s[0])+func_t(s[1]))*0.5)
            else:
                s = salary.split(pay_form)[1].split('元')[0]
                func_t = lambda x:int(x.strip().replace(',',''))
                return func_t(s)

        if '面議' in item['jobsalary']:
            item['jobsalary'] = 40000
        elif '月薪' in item['jobsalary']:
            item['jobsalary'] = salary_mean(item['jobsalary'],'月薪')
        elif '時薪' in item['jobsalary']:
            item['jobsalary'] = salary_mean(item['jobsalary'],'時薪')*160 # supposed working hours per month is 160 hours.

        # jobapply
        # divided into 3 class: class1 < 10 < class2 < 30 < class3
        ind_apply = int(item['jobapply'].split('~')[0].strip())
        if ind_apply <= 10:
            item['jobapply'] = 1
        elif ind_apply <= 30:
            item['jobapply'] = 2
        else:
            item['jobapply'] = 3

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
        return item

# class MongoDBPipline(object):
#     '''Write data to database
    
#     '''
#     def open_spider(self, spider):
#         db_uri = spider.settings.get('MONGODB_URI', 'mongodb://localhost:27017')
#         db_name = spider.settings.get('MONGO_DB_NAME', 'job_data')
#         self.db_client = MongoClient('mongodb://localhost:27017')
#         self.db = self.db_client[db_name]
        
#     def close_spider(self, spider):
#         self.db_client.close()
        
#     def process_item(self, item, spider):
#         self.insert_db(item)
        
#         return item
    
#     def insert_db(self, item):
#         item = dict(item)
#         self.db.job_data.insert_one(item)
        
        
        