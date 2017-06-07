# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
from doubanSpider.items import DoubanspiderItem

class DoubanuserSpider(scrapy.Spider):
    name = 'doubanuser'
    allowed_domains = ['www.douban.com']
    base_url='https://www.douban.com/group/559779/members?start='
    max_count=35
    start=0
    step=35

    def start_requests(self):
        while self.start<self.max_count:
            yield scrapy.Request(self.base_url+str(self.start),self.parse)
            self.start +=self.step

    def parse(self, response):
        userGroups = Selector(response).xpath('//div[@class="member-list"]')
        for group in userGroups:
            self.logger.info(group)
        #self.logger.info('******************* %s',response.url)
        pass
