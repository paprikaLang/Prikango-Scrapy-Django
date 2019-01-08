# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, TakeFirst, Join
import datetime
import re
from BoleSpider.settings import SQL_DATETIME_FORMAT, SQL_DATE_FORMAT


class BolespiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


def convert_date(value):
    try:
        create_date = datetime.datetime.strptime(value, "%Y/%m/%d").date()
    except Exception as e:
        create_date = datetime.datetime.now().date()

    return create_date


def filter_num(value):
    match_re = re.match(".*?(\d+).*", value)
    if match_re:
        nums = int(match_re.group(1))
    else:
        nums = 0

    return nums


def eliminate_comment_tag(value):
    # 去掉tag中提取的评论
    if "评论" in value:
        return ""
    else:
        return value


def eliminate_takeFirst(value):
    return value


class BolePostItemLoader(ItemLoader):
    # 自定义item loader
    default_output_processor = TakeFirst()


class BolePostItem(scrapy.Item):
    title = scrapy.Field()
    create_date = scrapy.Field(
        input_processor=MapCompose(convert_date)
    )
    url = scrapy.Field()
    url_object_id = scrapy.Field()
    preview_img = scrapy.Field(
        output_processor=MapCompose(eliminate_takeFirst)
    )
    preview_img_path = scrapy.Field()
    votes = scrapy.Field(
        input_processor=MapCompose(filter_num)
    )
    comments = scrapy.Field(
        input_processor=MapCompose(filter_num)
    )
    bookmarks = scrapy.Field(
        input_processor=MapCompose(filter_num)
    )
    tags = scrapy.Field(
        input_processor=MapCompose(eliminate_comment_tag),
        output_processor=Join(",")
    )
    body = scrapy.Field()

    def get_insert_sql(self):
        insert_sql = """
            insert into article(title, url, url_object_id, votes, body)
            VALUES(%s, %s, %s, %s, %s)
        """
        params = (self["title"], self["url"], self["url_object_id"], self["votes"], self["body"])

        return insert_sql, params


def remove_splash(value):
    # 去掉工作城市的斜线
    return value.replace("/","")


def handle_jobaddr(value):
    addr_list = value.split("\n")
    addr_list = [item.strip() for item in addr_list if item.strip()!="查看地图"]
    return "".join(addr_list)


class LagouJobItemLoader(ItemLoader):
    # 自定义itemloader
    default_output_processor = TakeFirst()


class LagouJobItem(scrapy.Item):
    # 拉勾网职位信息
    title = scrapy.Field()
    url = scrapy.Field()
    url_object_id = scrapy.Field()
    salary = scrapy.Field()
    job_city = scrapy.Field(
        input_processor=MapCompose(remove_splash),
    )
    work_years = scrapy.Field(
        input_processor=MapCompose(remove_splash),
    )
    degree_need = scrapy.Field(
        input_processor=MapCompose(remove_splash),
    )
    job_type = scrapy.Field()
    publish_time = scrapy.Field()
    job_advantage = scrapy.Field()
    job_desc = scrapy.Field()
    job_addr = scrapy.Field(
        input_processor=MapCompose(eliminate_comment_tag, handle_jobaddr),
    )
    company_name = scrapy.Field()
    company_url = scrapy.Field()
    tags = scrapy.Field(
        input_processor=Join(",")
    )
    crawl_time = scrapy.Field()

    def get_insert_sql(self):
        insert_sql = """
     insert into lagou(title, url, url_object_id, salary, city, publish_time, years) VALUES(%s, %s, %s, %s, %s, %s, %s)
        """
        params = (
         self["title"], self["url"], self["url_object_id"], self["salary"], self["job_city"], self["publish_time"],
         self["work_years"]
        )
        # self["crawl_time"].strftime(SQL_DATETIME_FORMAT),
        return insert_sql, params



