# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from urllib import parse
from BoleSpider.items import BolePostItem, BolePostItemLoader
from BoleSpider.utils.tools import to_md5


class JobboleSpider(scrapy.Spider):

    name = 'jobbole'
    allowed_domains = ['blog.jobbole.com']
    start_urls = ['http://blog.jobbole.com/all-posts/']

    def parse(self, response):
        page_posts_nodes = response.css("#archive .floated-thumb .post-thumb a")

        for post_node in page_posts_nodes:
            post_url = post_node.css("::attr(href)").extract_first("")
            image_url = post_node.css("img::attr(src)").extract_first("")
            yield Request(url=parse.urljoin(response.url, post_url), meta={"preview_img": image_url}, callback=self.parse_post)

        next_page_url = response.css(".next.page-numbers::attr(href)").extract_first("")
        if next_page_url:
            yield Request(url=parse.urljoin(response.url, next_page_url), callback=self.parse)

    def parse_post(self, response):

        preview_img = response.meta.get("preview_img", "")

        item_loader = BolePostItemLoader(item=BolePostItem(), response=response)
        item_loader.add_css("title", ".entry-header h1::text")
        item_loader.add_value("url", response.url)
        item_loader.add_value("url_object_id", to_md5(response.url))
        item_loader.add_css("create_date", "p.entry-meta-hide-on-mobile::text")
        item_loader.add_value("preview_img", [preview_img])
        item_loader.add_css("votes", ".vote-post-up h10::text")
        item_loader.add_css("comments", "a[href='#article-comment'] span::text")
        item_loader.add_css("bookmarks", ".bookmark-btn::text")
        item_loader.add_css("tags", "p.entry-meta-hide-on-mobile a::text")
        item_loader.add_css("body", "div.entry")

        post_item = item_loader.load_item()

        yield post_item









