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