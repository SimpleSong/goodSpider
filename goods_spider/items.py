# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ImageItemsItem(scrapy.Item):
    imageUrls = scrapy.Field()
    path = scrapy.Field()
    type = scrapy.Field()
    pass


class MongodbItem(scrapy.Item):
    url = scrapy.Field()  #商品链接
    name = scrapy.Field() #商品名称
    skuList = scrapy.Field()  #sku集合
    source = scrapy.Field() #来源
    brand = scrapy.Field() #品牌
    seller = scrapy.Field() #卖家
    mainPrice = scrapy.Field() #主价格
    prices = scrapy.Field() #价格
    details = scrapy.Field() #详情信息
    pass
