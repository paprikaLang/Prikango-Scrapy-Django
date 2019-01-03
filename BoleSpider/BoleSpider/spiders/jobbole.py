# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy.http import Request
from urllib import parse
from BoleSpider.items import BolePostItem
from BoleSpider.utils.tools import to_md5
import datetime

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
        post_item = BolePostItem()

        # css选择器
        title = response.css(".entry-header h1::text").extract_first().strip()
        create_date = response.css(".entry-meta-hide-on-mobile::text").extract_first().strip().replace("·", "").strip()
        votes = int(response.css(".vote-post-up h10::text").extract_first())
        bookmarks = response.css(".bookmark-btn::text").extract_first()
        match_re = re.match(".*?(\d+).*", bookmarks)
        if match_re:
            bookmarks = int(match_re.group(1))
        else:
            bookmarks = 0

        comments = response.css("a[href='#article-comment'] span::text").extract_first()
        match_re = re.match(".*?(\d+).*", comments)
        if match_re:
            comments = int(match_re.group(1))
        else:
            comments = 0

        body = response.css("div.entry").extract_first()

        tags = response.css("p.entry-meta-hide-on-mobile a::text").extract()
        tags = [el for el in tags if not el.strip().endswith("评论")]
        tags = ",".join(tags)
        preview_img = response.meta.get("preview_img", "")

        try:
            create_date = datetime.datetime.strptime(create_date, "%Y/%m/%d").date()
        except Exception as e:
            create_date = datetime.datetime.now().date()

        post_item["create_date"] = create_date
        post_item["title"] = title
        post_item["url"] = response.url
        post_item["preview_img"] = [preview_img]
        post_item["votes"] = votes
        post_item["comments"] = comments
        post_item["bookmarks"] = bookmarks
        post_item["body"] = body
        post_item["tags"] = tags
        post_item["url_object_id"] = to_md5(response.url)

        yield post_item


        # title = response.xpath('//*[@id="post-110287"]/div[1]/h1/text()').extract_first()
        # create_date = response.xpath("//p[@class='entry-meta-hide-on-mobile']/text()").extract_first().strip().replace("·", "").strip()
        # votes =response.xpath("//span[contains(@class, 'vote-post-up')]/h10/text()").extract_first()
        #
        # favs = response.xpath("//span[contains(@class, 'bookmark-btn')]/text()").extract_first()
        # match_re = re.match(".*?(\d+).*", favs)
        # if match_re:
        #     favs = match_re.group(1)
        #
        # comments = response.xpath("//a[@href='#article-comment']/span/text()").extract_first()
        # match_re = re.match(".*?(\d+).*", comments)
        # if match_re:
        #     comments = match_re.group(1)
        #
        # body = response.xpath("//div[@class='entry']").extract_first()
        # tags = response.xpath("//p[@class='entry-meta-hide-on-mobile']/a/text()").extract()
        # tags = [el for el in tags if not el.strip().endswith("评论")]
        # tags = ",".join(tags)









