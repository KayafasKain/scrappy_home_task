# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ShopParseItem(scrapy.Item):
    # define the fields for your item here like:
    ware_name = scrapy.Field()
    price = scrapy.Field()
    description = scrapy.Field()
    currency = scrapy.Field()
    brand = scrapy.Field()
    sizes = scrapy.Field()
    images = scrapy.Field()