## -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
import logging

from scrapy import Item, Spider, signals
from scrapy.crawler import Crawler
from scrapy.exceptions import NotConfigured


class ${class_name}:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    @classmethod
    def from_crawler(cls, crawler: Crawler):
        if not crawler.settings.getbool("${logger_name}_ENABLED"):
            raise NotConfigured

        ext = cls()

        crawler.signals.connect(ext.spider_opened, signal=signals.spider_opened)
        crawler.signals.connect(ext.spider_closed, signal=signals.spider_closed)
        crawler.signals.connect(ext.item_scraped, signal=signals.item_scraped)

        return ext

    def spider_opened(self, spider: Spider) -> None:
        pass

    def spider_closed(self, spider: Spider) -> None:
        pass

    def item_scraped(self, item: Item, spider: Spider) -> Item:
        pass
