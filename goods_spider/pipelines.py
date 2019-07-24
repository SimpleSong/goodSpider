# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.pipelines.images import ImagesPipeline
from scrapy import Request
from goods_spider.items import ImageItemsItem, MongodbItem

class ImageItemsPipeline(ImagesPipeline):
    # def process_item(self, item, spider):
    #     return item

    def file_path(self, request, response=None, info=None):
        path = request.meta['path']
        type = request.meta['type']
        image_guid = request.url.split('/')[-1]
        return path + '/' + type + '/' + image_guid.split('?')[0]


    def get_media_requests(self, item, info):

        if not type(item) == ImageItemsItem:
            return

        # 循环每一张图片地址下载，若传过来的不是集合则无需循环直接yield
        for image_url in item['imageUrls']:
            yield Request(image_url, meta={'path':item['path'],'type':item['type']})

import pymongo

class InputmongodbPipeline(object):
    def __init__(self):
        # 建立MongoDB数据库连接
        client = pymongo.MongoClient('127.0.0.1', 27017)
        # 连接所需数据库,ScrapyChina为数据库名
        db = client['items']
        # 连接所用集合，也就是我们通常所说的表，mingyan为表名
        self.post = db['items']

    def process_item(self, item, spider):

        if not type(item) == MongodbItem:
            return item

        postItem = dict(item)  # 把item转化成字典形式
        count = self.post.count({'url':postItem['url']})
        if count == 0:
            self.post.insert(postItem)  # 向数据库插入一条记录
        return item  # 会在控制台输出原item数据，可以选择不写