# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BothaiItem(scrapy.Item):
    coin = scrapy.Field()
    Time = scrapy.Field()
    price_btc = scrapy.Field()
    price_usd = scrapy.Field()
    volume_usd = scrapy.Field()
    market_cap_by_available_supply = scrapy.Field()