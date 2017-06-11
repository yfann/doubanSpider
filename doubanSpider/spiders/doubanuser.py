# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy.selector import Selector
from doubanSpider.items import *

class DoubanuserSpider(scrapy.Spider):
    name = 'doubanuser'
    allowed_domains = ['www.douban.com']
    group_member_url='https://www.douban.com/group/gogo/members?start={start}'
    user_groupjoin_url='https://www.douban.com/group/people/{userid}/joins'

    step=35
    page_count=995

    def start_requests(self):
        current_page=0
        while current_page<=self.page_count:
            self.logger.info('******* current page number:{} **********'.format(current_page))
            yield scrapy.Request(self.group_member_url.format(start=self.step*current_page),self.parse)
            current_page +=1

    def parse(self, response):
        #self.logger.info('******************* %s',response.url)
        users = Selector(response).xpath('//div[@class="member-list"]/ul/li')
        for user in users:
            item = UserItem()
            item['head_url']=user.xpath('.//div[@class="pic"]//img/@src').extract_first()
            item['user_name']=user.xpath('.//div[@class="name"]/a/text()').extract_first()
            item['user_url']=user.xpath('.//div[@class="name"]/a/@href').extract_first()
            item['user_id'] = re.findall(r'(\d+)/$',item['user_url'])[0]
            request = scrapy.Request(self.user_groupjoin_url.format(userid=item['user_id']),self.joinGroupParse)
            request.meta['item'] = item
            yield request
       

    def joinGroupParse(self,response):
        item = response.meta['item']
        groups = Selector(response).xpath('//div[contains(@class,"group-list")]/ul/li')
        group_list=[]
        for group in groups:
            g=UserGroupItem()
            g['group_name'] = group.xpath('.//div[@class="info"]/div[@class="title"]/a/@title').extract_first()
            g['group_url'] = group.xpath('.//div[@class="info"]/div[@class="title"]/a/@href').extract_first()
            g['group_num'] = group.xpath('.//div[@class="info"]/span[@class="num"]/text()').extract_first().replace('(','').replace(')','')
            group_list.append(g)
        item['joined_groups']=group_list
        yield item
