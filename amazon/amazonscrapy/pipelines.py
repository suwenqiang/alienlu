# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class AmazonscrapyPipeline(object):
    def __init__(self):
        self.file = open('amazone.csv','w')
        self.file.write('page')
        self.file.write(',')
        self.file.write('rank')
        self.file.write('\n')
        self.file1 = open('amazone.csv','a+')
    def process_item(self, item, spider):
        page = item['page']
        rank = item['rank']
        asin = item['asin']
        self.file1.write(page)
        self.file1.write(',')
        self.file1.write(rank)
        self.file1.write(',')
        self.file1.write(asin)
        self.file1.write('\n')
    
    def close_spider(self,spider):
        self.file.close()
        print 'spider close!' 