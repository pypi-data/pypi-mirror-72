# -*- coding: utf-8 -*-
import scrapy

from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, TakeFirst, Identity


class BaseItem(scrapy.Item):
    project = scrapy.Field()
    spider = scrapy.Field()
    server = scrapy.Field()
    date = scrapy.Field()

    id = scrapy.Field()
    language = scrapy.Field()
    address = scrapy.Field()
    address_length = scrapy.Field()
    content_type = scrapy.Field()
    title = scrapy.Field()
    canonical_version = scrapy.Field()
    title_length = scrapy.Field()
    description = scrapy.Field()
    description_length = scrapy.Field()
    keywords = scrapy.Field()
    h1 = scrapy.Field()
    h2 = scrapy.Field()
    loading_time = scrapy.Field()
    robot = scrapy.Field()
    status_code = scrapy.Field()
    content = scrapy.Field()
    hash = scrapy.Field()


class BaseItemLoader(ItemLoader):
    default_output_processor = TakeFirst()

    title_in = MapCompose(str.strip)
    h1_in = MapCompose(str.strip)
    h2_out = Identity()
