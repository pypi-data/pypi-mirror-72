from __future__ import annotations

import datetime
import socket
import hashlib
import scrapy
from scrapy.exceptions import CloseSpider

from abc import ABC, abstractmethod
from ..items import BaseItem, BaseItemLoader


class BaseSpider(ABC, scrapy.spiders.SitemapSpider):
    name = 'base'
    allowed_domains = []
    sitemap_urls = []
    content_container = '//body//text()'

    def start_requests(self):
        if not self.__has_permissions():
            raise CloseSpider(self.name)

        return super().start_requests()

    def parse(self, response):
        item_loader = BaseItemLoader(item=BaseItem(), response=response)

        address = response.url
        item_loader.add_value('id', self.__generate_id(address))
        item_loader.add_value('address', address)
        item_loader.add_value('address_length', len(address))
        item_loader.add_xpath('canonical_version', '/html/head/link[@rel="canonical"]/@href')
        item_loader.add_value('content_type', response.headers['Content-Type'].decode('utf-8'))
        item_loader.add_xpath('language', '/html/@lang')

        title = response.xpath('//title/text()').get()
        item_loader.add_value('title', title)
        item_loader.add_value('title_length', len(title))

        description = response.xpath('//meta[@name="Description" or @name="description"]/@content').get()
        item_loader.add_value('description', description)
        item_loader.add_value('description_length', len(description) if description else 0)
        item_loader.add_xpath('keywords', '//meta[@name="keywords"]/@content')
        item_loader.add_xpath('h1', '//h1//text()')
        item_loader.add_xpath('h2', '//h2//text()')
        item_loader.add_value('loading_time', response.meta['download_latency'])
        item_loader.add_xpath('robot', '//meta[@name="robots"]/@content')
        item_loader.add_value('status_code', response.status)

        content = response.xpath(self.content_container).getall()

        safe_content = ' '.join([' '.join(c.split()) for c in content if c.split()])

        item_loader.add_value('content', safe_content)
        item_loader.add_value('hash', self.__hash_content(safe_content))

        self.__generate_housekeeping_items(item_loader)
        self._add_custom_items(item_loader)

        yield item_loader.load_item()

    def __generate_housekeeping_items(self, item_loader):
        item_loader.add_value('project', self.settings.get('BOT_NAME'))
        item_loader.add_value('spider', self.name)
        item_loader.add_value('server', socket.gethostname())
        item_loader.add_value('date', datetime.datetime.now())

    @staticmethod
    def __generate_id(url: str):
        result = hashlib.md5(url.encode())

        return result.hexdigest()

    @staticmethod
    def __hash_content(content: str):
        result = hashlib.blake2b(content.encode())

        return result.hexdigest()

    @staticmethod
    def __has_permissions():
        return True

    @abstractmethod
    def _add_custom_items(self, item_loader: BaseItemLoader):
        raise NotImplementedError
