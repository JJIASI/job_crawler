import scrapy
from scrapy.selector import Selector
from urllib.parse import urlencode
from job_crawler.items import JobCrawlerItem

class Spider104(scrapy.Spider):
    name='crawler104'
    
    def url_get(page_n):
        data = {
            'ro': 0,
            'kwop': 7,
            'keyword': 'golang',
            'order': 1,
            'asc': 0,
            'page': page_n,
            'mode': 'l',  # 's' & 'l'
            'jobsource': '2018indexpoc'
        }
        urls = 'https://www.104.com.tw/jobs/search/?' + urlencode(data)
        return urls
    
    start_urls = [url_get(1)]
    
    def __init__(self):
        self.page_number = 1
        
    def parse(self, response):
        selector = Selector(response)
        jobname = selector.css('.js-job-link').xpath('@title').extract()
        jobdate = selector.css('.job-mode__date')[1:]
        jobcompany = selector.css('.job-mode__company').css('a::text').extract()
        jobexp = selector.css('.job-mode__exp::text').extract()[1:]
        jobedu = selector.css('.job-mode__edu::text').extract()[1:]
        jobarea = selector.css('.job-mode__area::text').extract()[1:]
        if jobname == 0:
            raise  CloseSpider('No more pages')
        for i in range(len(jobname)):
            if len(jobdate[i].xpath('.//text()').extract())==1:
                jobcrawleritem = JobCrawlerItem()
                jobcrawleritem['jobname'] = jobname[i]
                jobcrawleritem['jobdate'] = jobdate[i].xpath('.//text()').extract()[0].replace('\n','').strip()
                jobcrawleritem['jobcompany'] = jobcompany[i]
                jobcrawleritem['jobexp'] = jobexp[i]
                jobcrawleritem['jobedu'] = jobedu[i]
                jobcrawleritem['jobarea'] = jobarea[i]
                yield jobcrawleritem
        self.page_number += 1
        print(self.page_number)
        urls = Spider104.url_get(self.page_number)
        yield scrapy.Request(urls)