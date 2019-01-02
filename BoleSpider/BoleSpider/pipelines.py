# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.pipelines.images import ImagesPipeline
import codecs
import json
from scrapy.exporters import JsonItemExporter

class BolespiderPipeline(object):
    def process_item(self, item, spider):
        return item

class BoleJsonExporterPipeline(object):
    #自定义json文件导出
    def __init__(self):
        self.file = open('post_export.json', 'wb')
        self.exporter = JsonItemExporter(self.file, encoding='utf-8', ensure_ascii=False)
        self.exporter.start_exporting()
    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()
    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item

class BoleJsonWithEncodingPipeline:
    def __init__(self):
        self.file = codecs.open('post.json', 'w', encoding='utf-8')
    def process_item(self, item, spider):
        lines = json.dumps(dict(item), ensure_ascii=False) + "\n"
        self.file.write(lines)
        return item
    def spider_closed(self):
        self.file.close()

class BoleImagePipeline(ImagesPipeline):
    def item_completed(self, results, item, info):
        for ok, value in results:
             item["preview_img_path"] = value["path"]
        return item