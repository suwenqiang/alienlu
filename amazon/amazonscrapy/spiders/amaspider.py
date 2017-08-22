import scrapy
from amazonscrapy.items import AmazonscrapyItem
import re
import time



class AmaSpider(scrapy.Spider):
    name = 'ama'
    allowed_domains = ['www.amazon.com']
    def __init__(self):
        self.key = {}
        with open('keyword.csv','r') as a:
            for x in a.readlines():
                x = x.strip('\n').split(',')
                self.key[x[0]] = x[1]
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'}


    def start_requests(self):
        for x in self.key:                                                                                                        
            url = 'http://www.amazon.com/s/ref=nb_sb_noss_2?url=search-alias%3Daps&field-keywords=' + str(x)
            yield scrapy.Request(url=url,headers=self.headers,meta={"asin":self.key[x]})
            time.sleep(1)


    def parse(self, response):
        item = AmazonscrapyItem()
        next_url = 'http://www.amazon.com' + str(response.xpath('//*[@id="pagnNextLink"]/@href').extract()[0])
        rank = response.xpath('//*[@data-asin=%s]/@id'%('"' + response.meta['asin'] + '"'))
        if rank:
            #item['page'] = soup.find("span",attrs={"class":"pagnCur"}).string
            item['page'] = response.xpath('//*[@class="pagnCur"]/text()').extract()[0]
            item['rank'] = rank.extract()[0]
            item['asin'] = response.meta['asin']
            yield item
            print 'find it!',item['page'], item['rank'],response.meta['asin']
        else:
            print 'Not found,' + response.meta['asin'] + ',' + 'searching next page'
            time.sleep(1)
            yield scrapy.Request(url=next_url,callback=self.parse,meta={"asin":response.meta['asin']})