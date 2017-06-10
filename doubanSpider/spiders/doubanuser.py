# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy.selector import Selector
from doubanSpider.items import DoubanspiderItem

class DoubanuserSpider(scrapy.Spider):
    name = 'doubanuser'
    allowed_domains = ['www.douban.com']
    group_member_url='https://www.douban.com/group/559779/members?start={start}'
    user_groupjoin_url='https://www.douban.com/group/people/{userid}/joins'

    start=0
    step=35

    max_count=35

    def start_requests(self):
        while self.start<self.max_count:
            yield scrapy.Request(self.group_member_url.format(start=self.start),self.parse)
            self.start +=self.step

    def parse(self, response):
        users = Selector(response).xpath('//div[@class="member-list"]/ul/li')
        item = DoubanspiderItem()
        for user in users:
            item['head_url']=user.xpath('.//div[@class="pic"]//img/@src').extract_first()
            item['user_name']=user.xpath('.//div[@class="name"]/a/text()').extract_first()
            item['user_url']=user.xpath('.//div[@class="name"]/a/@href').extract_first()
            item['user_id'] = re.findall(r'(\d+)/$',item['user_url'])[0]
            request = scrapy.Request(self.user_groupjoin_url.format(userid=item['user_id']),self.joinGroupParse)
            request.meta['item'] = item
            yield request
        #self.logger.info('******************* %s',response.url)

    def joinGroupParse(self,response):
        item = response.meta['item']
        groups = Selector(response).xpath('//div[contains(@class,"group-list")]/ul/li')
        group_list=[]
        for group in groups:
            group_name = group.xpath('.//div[@class="info"]/div[@class="title"]/a/@title').extract_first()
            group_url = group.xpath('.//div[@class="info"]/div[@class="title"]/a/@href').extract_first()
            group_num = group.xpath('.//div[@class="info"]/span[@class="num"]/text()').extract_first().replace('(','').replace(')','')
            g={
                'group_name':group_name,
                'group_url':group_url,
                'group_num':group_num
            }
            group_list.append(g)

        item['joined_groups']=group_list
        yield item
