# -*- coding: utf-8 -*-
import scrapy
from selenium import webdriver
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals
from scrapy.http import Request
from urllib import parse
from BoleSpider.items import LagouJobItemLoader, LagouJobItem
from BoleSpider.utils.tools import to_md5
import datetime

class LagouSpider(scrapy.Spider):
    name = 'lagou'
    allowed_domains = ['www.lagou.com']
    start_urls = ['https://www.lagou.com']

    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        self.browser = webdriver.Chrome()
        super(LagouSpider, self).__init__()
        dispatcher.connect(self.spider_closed, signals.spider_closed)

    def spider_closed(self, spider):
        print("spider closed now")
        self.browser.quit()

    def parse(self, response):
        zhaopin_url = response.css(".sidebar .mainNavs .menu_box:nth-child(1) .menu_main .category-list a::attr(href)").extract_first()
        # for zhaopin_url in zhaopin_urls:
        yield Request(url=parse.urljoin(response.url, zhaopin_url), callback=self.parse_language)

    def parse_language(self, response):
        jobs_urls = response.css(".s_position_list .list_item_top .position .p_top a::attr(href)").extract()
        for job_url in jobs_urls:
            yield Request(url=parse.urljoin(response.url, job_url), callback=self.parse_job)

    def parse_job(self, response):
        print('parse: ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
        item_loader = LagouJobItemLoader(item=LagouJobItem(), response=response)
        item_loader.add_css("title", ".job-name::attr(title)")
        item_loader.add_value("url", response.url)
        item_loader.add_value("url_object_id", to_md5(response.url))
        item_loader.add_css("salary", ".job_request .salary::text")
        item_loader.add_xpath("job_city", "//*[@class='job_request']/p/span[2]/text()")
        item_loader.add_xpath("work_years", "//*[@class='job_request']/p/span[3]/text()")
        item_loader.add_xpath("degree_need", "//*[@class='job_request']/p/span[4]/text()")
        item_loader.add_xpath("job_type", "//*[@class='job_request']/p/span[5]/text()")

        item_loader.add_css("tags", '.position-label li::text')
        item_loader.add_css("publish_time", ".publish_time::text")
        item_loader.add_css("job_advantage", ".job-advantage p::text")
        item_loader.add_css("job_desc", ".job_bt div")
        item_loader.add_css("job_addr", ".work_addr")
        item_loader.add_css("company_name", "#job_company dt a img::attr(alt)")
        item_loader.add_css("company_url", "#job_company dt a::attr(href)")
        item_loader.add_value("crawl_time", datetime.datetime.now())
        yield item_loader.load_item()

