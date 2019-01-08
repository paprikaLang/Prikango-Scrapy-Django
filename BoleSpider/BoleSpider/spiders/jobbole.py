# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from urllib import parse
from BoleSpider.items import BolePostItem, BolePostItemLoader
from BoleSpider.utils.tools import to_md5
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals

class JobboleSpider(scrapy.Spider):

    name = 'jobbole'
    allowed_domains = ['blog.jobbole.com']
    start_urls = ['http://blog.jobbole.com/all-posts/']

    # 收集不同状态码下的页面信息 301 302 200...
    handle_httpstatus_list = [404]

    def __init__(self, **kwargs):
        self.fail_urls = []
        dispatcher.connect(self.handle_spider_closed, signals.spider_closed)

    def handle_spider_closed(self, spider, reason):
        self.crawler.stats.set_value("failed_urls", ",".join(self.fail_urls))

    def parse(self, response):

        if response.status == 404:
            self.fail_urls.append(response.url)
            self.crawler.stats.inc_value("failed_url")

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









