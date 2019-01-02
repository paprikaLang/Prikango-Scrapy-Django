# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BolespiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class BolePostItem(scrapy.Item):
    title = scrapy.Field()
    create_date = scrapy.Field()
    url = scrapy.Field()
    url_object_id = scrapy.Field()
    preview_img = scrapy.Field()
    preview_img_path = scrapy.Field()
    votes = scrapy.Field()
    comments = scrapy.Field()
    bookmarks = scrapy.Field()
    tags = scrapy.Field()
    body = scrapy.Field()