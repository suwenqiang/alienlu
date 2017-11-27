# -*- coding: utf-8 -*-
import scrapy
import requests
import time
import json
import MySQLdb
import re
from ..items import BothaiItem


def createdatabase():
    #连接数据库
    try:
        conn = MySQLdb.connect(host='', port=3306, user='root', passwd='')#host为数据库IP，passwd为数据库密码
        cur = conn.cursor()
    except:
        print u'连接数据库失败'
    try:
        cur.execute('create database if not exists both_ai DEFAULT CHARSET utf8 COLLATE utf8_general_ci')
    except:
        print u'创建数据库失败'


def database(coin):
    #连接数据库
    try:
        conn = MySQLdb.connect(host='', port=3306, user='root', passwd='',db='both_ai')#host为数据库IP，passwd为数据库密码
        cur = conn.cursor()
    except:
        print u'连接数据库失败'
    # 创建表
    try:
        cur.execute("CREATE TABLE " + str(coin) + " (Time VARCHAR(20), market_cap_by_available_supply float(20,10), price_btc float(20,10), price_usd float(20,10), volume_usd float(20,10))")
    except:
        print u'创建表失败',coin


class BothaiSpider(scrapy.Spider):
    name = "bothai"
    allowed_domains = ["coinmarketcap.com"]
    start_urls = ['http://coinmarketcap.com/']

    def __init__(self):
        self.headers = {'accept':'application/json, text/javascript, */*; q=0.01',
                        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 MicroMessenger/6.5.2.501 NetType/WIFI WindowsWechat QBCore/3.43.691.400 QQBrowser/9.0.2524.400',
                        'Accept-Encoding': 'gzip, deflate',
                        'Accept-Language': 'zh-CN,zh;q=0.8,en-us;q=0.6,en;q=0.5;q=0.4',}
        coin_list_url = 'https://files.coinmarketcap.com/generated/search/quick_search.json'
        coin_html = requests.get(url=coin_list_url,headers=self.headers).json()
        coin_list = [x['slug'].lower() for x in coin_html]
        database_coinname_list = [x.replace('-', '_')+'_table' for x in coin_list]
        st = '2014-02-14 00:00:00'  # 例如2016-05-05 20:28:54
        et = '2017-11-26 00:00:00'
        stimeArray = time.strptime(st, "%Y-%m-%d %H:%M:%S")
        stimestamp = int(time.mktime(stimeArray)) * 1000
        etimeArray = time.strptime(et, "%Y-%m-%d %H:%M:%S")
        etimestamp = int(time.mktime(etimeArray)) * 1000
        createdatabase()#创建数据库
        self.database = [database(name) for name in database_coinname_list]#创建表
        self.all_url_list = []
        for coin in coin_list:
            a = stimestamp
            for t in range((etimestamp-stimestamp)/86400000+1):
                url = 'https://graphs.coinmarketcap.com/currencies/' + str(coin) + '/' + str(a) + '/' + str(a + 86400000)
                self.all_url_list.append(url)
                a = a + 86400000
        print u'总共需要爬取的页面数为',len(self.all_url_list)


    def start_requests(self):
        for url in self.all_url_list:
            coin_name = re.search(r'.*?/currencies/(.*?)/',url).group(1)
            print u'爬取币种',coin_name, url
            yield scrapy.Request(url=url, headers=self.headers, callback=self.parse,meta={'coin_name':coin_name})


    def parse(self, response):
        result = json.loads(response.body)
        item = BothaiItem()
        item['coin'] = response.meta['coin_name'].replace('-', '_') + '_table'
        for (w, x, y, z) in zip(result['volume_usd'], result['price_usd'], result['price_btc'],result['market_cap_by_available_supply']):
            time_local = time.localtime(int(int(w[0]) / 1000))
            item['Time'] = time.strftime("%Y-%m-%d %H:%M:%S", time_local)
            item['volume_usd'] = w[1]
            item['price_usd'] = x[1]
            item['price_btc'] = y[1]
            item['market_cap_by_available_supply'] = z[1]
            yield item
