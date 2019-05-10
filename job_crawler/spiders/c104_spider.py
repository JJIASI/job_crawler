import scrapy
from scrapy.selector import Selector
from urllib.parse import urlencode
from job_crawler.items import JobCrawlerItem

class Spider104(scrapy.Spider):
    name='crawler104'
    keyword = input("Enter the keyword to be 104 scrape: ")

    def __init__(self):
        self.page_number = 1

    def url_get(page_n, keyword):
        data = {
            'ro': 0,
            'kwop': 7,
            'keyword': keyword,
            'order': 1,
            'asc': 0,
            'page': page_n,
            'mode': 's',  # 's' & 'l'
            'jobsource': '2018indexpoc'
        }
        urls = 'https://www.104.com.tw/jobs/search/?' + urlencode(data)
        return urls
    
    start_urls = [url_get(1, keyword)]
    
    def parse(self, response):
        selector = Selector(response)
        jobsalary = selector.xpath('//div/span[1]/text()').extract()
        jobname = selector.xpath('//article/@data-job-name').extract()
        jobcompany = selector.xpath('//article/@data-cust-name').extract()
        jobexp = selector.xpath('//div/ul[2]/li[2]/text()')[5:].extract()
        jobedu = selector.xpath('//div/ul[2]/li[3]/text()')[2:].extract()
        jobarea = selector.xpath('//div/ul[2]/li[1]/text()')[5:].extract()
        jobindcat = selector.xpath('//article/@data-indcat-desc').extract()
        jobapply = selector.xpath('.//div/a/text()')[2:-6].extract()
        jobdate = selector.css('.b-tit__date')[3:]
        if len(jobname) == 0:
            raise  print('No more pages')
        
        n = 0
        for i in range(len(jobname)):
            if len(jobdate[i].xpath('.//text()').extract())==1:
                if jobcompany[i] == '104外包網' or jobcompany[i] == '104家教網':
                    n +=1
                else:
                    i_n = i-n
                    jobcrawleritem = JobCrawlerItem()
                    jobcrawleritem['jobname'] = jobname[i]
                    jobcrawleritem['jobsalary'] = jobsalary[i_n]
                    jobcrawleritem['jobindcat'] = jobindcat[i]
                    jobcrawleritem['jobdate'] = jobdate[i].xpath('.//text()').extract()[0].replace('\n','').strip()
                    jobcrawleritem['jobcompany'] = jobcompany[i]
                    jobcrawleritem['jobexp'] = jobexp[i]
                    jobcrawleritem['jobedu'] = jobedu[i_n]
                    jobcrawleritem['jobarea'] = jobarea[i]
                    jobcrawleritem['jobapply'] = jobapply[i_n]
                    jobcrawleritem['sourceweb'] = '104人力銀行'
                    jobcrawleritem['keyword'] = self.keyword
                    yield jobcrawleritem
                
        self.page_number += 1
        if self.page_number > 50:
            raise  print('50 sheets complete!')
        print(f"第{self.page_number}頁")
        urls = Spider104.url_get(self.page_number, self.keyword)
        yield scrapy.Request(urls)