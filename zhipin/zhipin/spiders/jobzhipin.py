# -*- coding: utf-8 -*-
import time

import scrapy
from scrapy.selector.unified import SelectorList
from  zhipin.items import ZhipinItem


class JobzhipinSpider(scrapy.Spider):
    name = 'jobzhipin'
    allowed_domains = ['www.51job.com']  # 允许爬取的域名
    start_urls = ['https://search.51job.com/list/000000,000000,0000,00,9,99,python,2,1.html?lang=c&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&ord_field=0&dibiaoid=0&line=&welfare=']  # 第一次请求的页面

    def parse(self, response):

        job_infos = response.xpath('//*[@id="resultList"]/div[@class="el"]')

        for job in job_infos:
            item = ZhipinItem()
            Company = job.xpath(('./span[1]/a/text()')).get()
            Region = job.xpath('./span[2]/text()').get()
            Salary = job.xpath('./span[3]/text()').get()
            Position = job.xpath('./p/span/a/text()').extract_first().strip()
            # Position = job.xpath('./p/span/a/text()').extract_first()

            item['Company'] = Company
            item['Region'] = Region
            item['Salary'] = Salary
            item['Position'] = Position
            yield item

        #爬取下一页
        url ='https://search.51job.com/list/000000,000000,0000,00,9,99,python,2,%d.html?lang=c&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&ord_field=0&dibiaoid=0&line=&welfare='
        for i in range(1, 4):
            next_url = url % (i*1)
            yield scrapy.Request(url=next_url, callback=self.parse)
            time.sleep(5)


