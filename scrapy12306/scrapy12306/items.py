# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Scrapy12306Item(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    secertstr = scrapy.Field()
    train_no = scrapy.Field()
    checi = scrapy.Field()
    from_stationcode = scrapy.Field()
    to_stationcode = scrapy.Field()
    yp_info = scrapy.Field()
    train_location = scrapy.Field()
    train_date = scrapy.Field()
    back_train_date = scrapy.Field()
    query_from_station_name = scrapy.Field()
    query_to_station_name = scrapy.Field()
