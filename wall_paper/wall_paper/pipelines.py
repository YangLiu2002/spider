# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import scrapy
from scrapy.pipelines.images import ImagesPipeline
import os


class WallPaperPipeline(ImagesPipeline):

    def get_media_requests(self, item, info):
        img_url = item['img_url']
        yield scrapy.Request(img_url)

    def file_path(self, request, response=None, info=None, *, item=None):
        file_name = item['img_name'] + '.' + request.url.split('.')[-1]
        print(file_name, '下载成功!')

        return file_name

    def item_completed(self, results, item, info):
        return item
