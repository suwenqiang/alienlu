# -*- coding: utf-8 -*-
import scrapy
import requests
#import PyV8
import re
import time
import json
import os
import datetime
import random
from login import guahao
from smtp import send_mail
from mouse import click


def ck():
    while 1:
        s = requests.session()
        url = 'https://weixin.91160.com/?cid=23&auto_login=true&referrer=A91160&code=021bBIRb13U3as0Pk0Rb1YdCRb1bBIRS&state=91160'
        cookies = {
            'SHADOWMAN': '%7B%22key%22%3A%226709e794244ff436ce7aa95d9c1ff755%22%2C%22val%22%3A%22f46afa9edbd0d1dc5e3b150a1503388d%22%2C%22tm%22%3A1506309238%7D'}
        headers = {'Host': 'weixin.91160.com',
                   'Connection': 'keep-alive',
                   'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 MicroMessenger/6.5.2.501 NetType/WIFI WindowsWechat QBCore/3.43.691.400 QQBrowser/9.0.2524.400',
                   'X-Requested-With': 'XMLHttpRequest',
                   'Accept-Encoding': 'gzip, deflate',
                   'Accept-Language': 'zh-CN,zh;q=0.8,en-us;q=0.6,en;q=0.5;q=0.4'}
        # html = s.get(url=url, headers=headers)
        # js_func_string = re.search(r'.*?<script>(.*?)</script>', html.content).group(1).replace('eval(y', "String(y")
        # ctxt = PyV8.JSContext()
        # ctxt.enter()
        # c = ctxt.eval("""{js}""".format(js=js_func_string))
        # try:
        #     part1 = re.search(r'\{\};(var cd.*?var h\=).*?', c).group(1)
        #     part2 = re.search(r'.*?(return function\(x\).*?dc\+\=cd;).*?', c).group(1)
        #     part3 = part1 + "'x';" + part2
        #     d = part3 + 'String(dc);'
        #     e = ctxt.eval("""{js}""".format(js=d))
        #     cookie = {e.split('=')[0]: e.split('=')[1], html.cookies.keys()[0]: html.cookies.values()[0],
        #               'SHADOWMAN': '%7B%22key%22%3A%220cdfd3e5fd50b4bfbcd32176797cb56a%22%2C%22val%22%3A%2224bef379a5ee9d1e413230c83320de59%22%2C%22tm%22%3A1506136670%7D',
        #               'sms_mobile': '134****5165'}
        # except:
        #     part = re.search('\{\};(var.*?\+=cd;).*?', c).group(1)
        #     e = ctxt.eval("""{js}""".format(js=part))
        #     cookie = {e.split('=')[0]: e.split('=')[1], html.cookies.keys()[0]: html.cookies.values()[0],
        #               'SHADOWMAN': '%7B%22key%22%3A%220cdfd3e5fd50b4bfbcd32176797cb56a%22%2C%22val%22%3A%2224bef379a5ee9d1e413230c83320de59%22%2C%22tm%22%3A1506136670%7D',
        #               'sms_mobile': '134****5165'}
        if s.get(url=url, headers=headers, verify=False, cookies=cookies).status_code == 200:
            return cookies


class GuahaoSpider(scrapy.Spider):
    name = "guahao"
    allowed_domains = ["91160.com"]
    start_urls = ['http://91160.com/']

    def __init__(self,date=None):
        self.to_date = date.split(',')
        self.time_type = 'pm'
        self.headers ={'Host': 'weixin.91160.com',
                   'Connection': 'keep-alive',
                   'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 MicroMessenger/6.5.2.501 NetType/WIFI WindowsWechat QBCore/3.43.691.400 QQBrowser/9.0.2524.400',
                   'X-Requested-With': 'XMLHttpRequest',
                   'Accept-Encoding': 'gzip, deflate',
                   'Accept-Language': 'zh-CN,zh;q=0.8,en-us;q=0.6,en;q=0.5;q=0.4'}
        self.id = {}
        with open('ips.txt', 'r') as a:
            self.ip = a.readlines()[0].split(',')
        print self.to_date
        self.cookie = ck()


    def start_requests(self):
        while 1:
            url_accont = 'https://' + random.choice(self.ip) + '/doctor/schedule.html?unit_id=105&dep_id=2353&doctor_id=18157'
            yield scrapy.Request(url=url_accont, headers=self.headers, cookies=self.cookie, callback=self.parse,dont_filter=True,meta={'url': url_accont})


    def parse(self, response):
        if response.status != 200:
            self.cookie = ck()
        try:
            for x in json.loads(response.body)['data']['sch']:
                    if x['to_date'] in self.to_date and x['y_state'] == '1':
                        self.id['unit_id'] = x['unit_id']
                        self.id['doctor_id'] = x['doctor_id']
                        self.id['dep_id'] = x['dep_id']
                        self.id['sch_id'] = x['schedule_id']
                        print u'有号可以挂了',x['to_date'],x['time_type'],x['y_state'],datetime.datetime.now()
                        state,msg= guahao(self.id,self.cookie)
                        if state == 1:
                            print state,msg
                            send_mail(msg)
                            print datetime.datetime.now()
                            os._exit(0)
            print response.meta['url']
            print u'无号', datetime.datetime.now(),self.to_date,response.status
        except:
            print u'sch为空',self.to_date,response.status,response.body
            send_mail('need auth')
            time.sleep(60)