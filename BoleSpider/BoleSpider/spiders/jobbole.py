# -*- coding: utf-8 -*-
import scrapy
import re

class JobboleSpider(scrapy.Spider):
    name = 'jobbole'
    allowed_domains = ['blog.jobbole.com']
    start_urls = ['http://blog.jobbole.com/110287/']

    def parse(self, response):
        title = response.xpath('//*[@id="post-110287"]/div[1]/h1/text()').extract_first()
        create_date = response.xpath("//p[@class='entry-meta-hide-on-mobile']/text()").extract_first().strip().replace("·", "").strip()
        votes =response.xpath("//span[contains(@class, 'vote-post-up')]/h10/text()").extract_first()

        favs = response.xpath("//span[contains(@class, 'bookmark-btn')]/text()").extract_first()
        match_re = re.match(".*?(\d+).*", favs)
        if match_re:
            favs = match_re.group(1)

        comments = response.xpath("//a[@href='#article-comment']/span/text()").extract_first()
        match_re = re.match(".*?(\d+).*", comments)
        if match_re:
            comments = match_re.group(1)

        body = response.xpath("//div[@class='entry']").extract_first()
        tags = response.xpath("//p[@class='entry-meta-hide-on-mobile']/a/text()").extract()
        tags = [el for el in tags if not el.strip().endswith("评论")]
        tags = ",".join(tags)

        # css选择器
        title = response.css(".entry-header h1::text").extract_first().strip()
        create_date = response.css(".entry-meta-hide-on-mobile::text").extract_first().strip().replace("·", "").strip()
        votes = response.css(".vote-post-up h10::text").extract_first()
        bookmarks = response.css(".bookmark-btn::text").extract_first()
        match_re = re.match(".*?(\d+).*", bookmarks)
        if match_re:
            bookmarks = match_re.group(1)

        comments = response.css("a[href='#article-comment'] span::text").extract_first()
        match_re = re.match(".*?(\d+).*", comments)
        if match_re:
            comments = match_re.group(1)

        body = response.css("div.entry").extract_first()

        tags = response.css("p.entry-meta-hide-on-mobile a::text").extract()
        tags = [el for el in tags if not el.strip().endswith("评论")]
        tags = ",".join(tags)
        pass














