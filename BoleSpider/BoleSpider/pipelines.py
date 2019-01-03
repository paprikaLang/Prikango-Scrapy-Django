# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.pipelines.images import ImagesPipeline
import codecs
import json
from scrapy.exporters import JsonItemExporter
import MySQLdb
import MySQLdb.cursors
from twisted.enterprise import adbapi


class BoleSpiderPipeline(object):

    def process_item(self, item, spider):

        return item


class MysqlTwistedPipeline(object):
    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        dbparms = dict(
            host=settings["MYSQL_HOST"],
            db=settings["MYSQL_DBNAME"],
            user=settings["MYSQL_USER"],
            passwd=settings["MYSQL_PASSWORD"],
            charset='utf8',
            cursorclass=MySQLdb.cursors.DictCursor,
            use_unicode=True
        )
        dbpool = adbapi.ConnectionPool("MySQLdb", **dbparms)
        return cls(dbpool)

    def process_item(self, item, spider):
        query = self.dbpool.runInteraction(self.to_insert, item)
        query.addErrback(self.handle_error)

    def handle_error(self, failure):
        print(failure)

    def to_insert(self, cursor, item):

        insert_sql = """
                    insert into article(title, url, url_object_id, votes, body)
                    VALUES(%s, %s, %s, %s, %s)
                """
        cursor.execute(insert_sql, (item["title"], item["url"], item["url_object_id"], item["votes"], item["body"]))


class BoleJsonExporterPipeline(object):
    # 自定义json文件导出
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