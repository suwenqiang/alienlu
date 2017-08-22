# -*- coding: utf-8 -*-
import scrapy
from ama.items import AmazoneItem
from scrapy.http import Request
from bs4 import BeautifulSoup



class amazonespider(scrapy.Spider):
    name = "amazon"
    allowed_domain = ["amazon.com"]
    start_urls = ["https://www.amazon.com"]
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36'}


    def start_requests(self):
        for x in range(1,3):
            url = "https://www.amazon.com/s/ref=nb_sb_noss?url=search-alias%3Daps&field-keywords=iphone&page=" + str(x)
            yield Request(url=url,callback=self.parse)

    def parse(self,response):
        html = response.body
        soup = BeautifulSoup(html,"html.parser")
        item = AmazoneItem()
        item['item_name'] = soup.findAll('h2',attrs={'data-max-rows':"2"})
        item['price'] = soup.findAll('span',attrs={'class':'sx-price-whole'})
        item['url'] = soup.findAll('a',attrs={'class':'a-link-normal s-access-detail-page  a-text-normal'})
        return item

        #next_urls = soup.findAll('span',attrs={'class':'pagnLink'})
        #for url in next_urls:
        #    for x in url.children:
#        yield Request(url=x['href'],callback=self.parse)
