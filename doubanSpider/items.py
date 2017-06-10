# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DoubanspiderItem(scrapy.Item):
    user_id = scrapy.Field()
    user_name = scrapy.Field()
    user_url = scrapy.Field()
    head_url = scrapy.Field()
    joined_groups = scrapy.Field()
