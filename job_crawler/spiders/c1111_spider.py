import scrapy
from scrapy.selector import Selector
from urllib.parse import urlencode
from job_crawler.items import JobCrawlerItem

class Spider1111(scrapy.Spider):
    name='crawler1111'
    
    def url_get(page_n):
        data = {
            'si': 1,
            'ss': 'l',
            'ks': 'golang', 
            'pt': 0,
            'page': page_n
        }
        urls = 'https://www.1111.com.tw/job-bank/job-index.asp?' + urlencode(data)
        return urls
    
    start_urls = [url_get(1)]
    
    def __init__(self):
        self.page_number = 1
        
    def parse(self, response):
        selector = Selector(response)
        jobsalary = selector.css('.mnone::text').extract()
        jobname = selector.css('.mobiFullLInk').xpath('@title').extract()
        jobcompany = selector.xpath('//h4/a/text()').extract()
        jobexp = selector.css('.needs').xpath('text()[1]').extract()
        jobedu = selector.css('.needs').xpath('text()[2]').extract()
        jobarea = selector.css('.location>a::text').extract()
        jobindcat = selector.css('.csort>a::text').extract()
        jobdate = selector.css('.date>span::text').extract()
        jobapply = selector.css('.recruit>a::text').extract()
        if len(jobname) == 0:
            raise  print('No more pages')
        for i in range(len(jobname)):
                jobcrawleritem = JobCrawlerItem()
                jobcrawleritem['jobname'] = jobname[i]
                jobcrawleritem['jobsalary'] = jobsalary[i]
                jobcrawleritem['jobindcat'] = jobindcat[i]
                jobcrawleritem['jobdate'] = jobdate[i]
                jobcrawleritem['jobcompany'] = jobcompany[i]
                jobcrawleritem['jobexp'] = jobexp[i]
                jobcrawleritem['jobedu'] = jobedu[i]
                jobcrawleritem['jobarea'] = jobarea[i]
                jobcrawleritem['jobapply'] = jobapply[i]
                jobcrawleritem['sourceweb'] = '1111人力銀行'
                yield jobcrawleritem
                
        self.page_number += 1
        print(f"第{self.page_number}頁")
        urls = Spider1111.url_get(self.page_number)
        yield scrapy.Request(urls)