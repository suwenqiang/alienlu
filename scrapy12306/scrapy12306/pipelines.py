# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy12306.login import login

class Scrapy12306Pipeline(object):
    def process_item(self, item, spider):
        return item
        # secertstr = item['secertstr']
        # train_no = item['train_no']
        # checi = item['checi']
        # from_stationcode = item['from_stationcode']
        # to_stationcode = item['to_stationcode']
        # yp_info = item['yp_info']
        # train_location = item['train_location']
        # train_date = item['train_date']
        # back_train_date = item['back_train_date']
        # query_from_station_name = item['query_from_station_name']
        # query_to_station_name = item['query_to_station_name']
        # yield login(secertstr, train_no, checi, from_stationcode, to_stationcode, yp_info, train_location, train_date,
        #       back_train_date, query_from_station_name, query_to_station_name)
