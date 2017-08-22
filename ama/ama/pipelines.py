# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class AmaPipeline(object):
    def __init__(self):
        self.file = open('amazon.csv', 'w')
    def process_item(self, item, spider):
        name = item['item_name']
        price = item['price']
        url = item['url']
        for (x,y,z) in zip(name,price,url):
            self.file.write(x)
            self.file.write(',')
            self.file.write(y)
            self.file.write('\n')
    def close_spider(self, spider):
        print 'spider close'
        self.file.close()