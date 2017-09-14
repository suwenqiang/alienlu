# -*- coding: utf-8 -*-
import scrapy
import requests
import PyV8
import re
import time
import json
import os
import datetime
import random
from login import guahao
from smtp import send_mail

class GuahaoSpider(scrapy.Spider):
    name = "guahao"
    allowed_domains = ["91160.com"]
    start_urls = ['http://91160.com/']

    def __init__(self):
        self.to_date = ['2017-08-29','2017-08-30']
        self.time_type = 'am'
        self.headers = {'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Mobile Safari/537.36',
                        'Host':'wap.91160.com'}
        self.id = {}
        with open('ips.txt', 'r') as a:
            self.ip = a.readlines()[0].split(',')
        print self.to_date

        ##获取动态js，构造cookies
        url = 'https://wap.91160.com'
        html = requests.get(url=url, headers=self.headers)
        js_func_string = re.search(r'.*?<script>(.*?)</script>', html.content).group(1).replace('eval(y', "String(y")
        ctxt = PyV8.JSContext()
        ctxt.enter()
        c = ctxt.eval("""{js}""".format(js=js_func_string))
        part = re.search('\{\};(var.*?\+=cd;).*?', c).group(1)
        d = part + 'String(dc);'
        e = ctxt.eval("""{js}""".format(js=d))
        self.cookie = {e.split('=')[0]: e.split('=')[1],html.cookies.keys()[0]:html.cookies.values()[0]}

    def start_requests(self):
        while 1:
            url_accont = 'https://' + random.choice(self.ip) + '/doctor/schedule.html?unit_id=131&dep_id=769&doctor_id=18241'
            yield scrapy.Request(url=url_accont, headers=self.headers, cookies=self.cookie, callback=self.parse,dont_filter=True,meta={'url': url_accont})
            time.sleep(1)
    def parse(self, response):
        try:
            for x in json.loads(response.body)['data']['sch']:
                    if x['to_date'] in self.to_date and x['time_type'] == self.time_type and x['y_state'] == '1':
                        self.id['unit_id'] = x['unit_id']
                        self.id['doctor_id'] = x['doctor_id']
                        self.id['dep_id'] = x['dep_id']
                        self.id['sch_id'] = x['schedule_id']
                        print u'有号可以挂了',x['to_date'],x['time_type'],x['y_state']
                        result = guahao(self.id)
                        while result == -4:
                            print result
                            time.sleep(1)
                            guahao(self.id,self.cookie)
                            send_mail()
                        os._exit(0)
            print response.meta['url']
            print u'无号', datetime.datetime.now(), json.loads(response.body)['data']['sch'][0]['y_state_desc']
        except:
            print u'sch为空'