# -*- coding: utf-8 -*-
import scrapy
import datetime
import random
from station import station
import time
import json
import os
from login import *
from smtp import send_mail

class A12306Spider(scrapy.Spider):
    name = "12306"
    allowed_domains = ["kyfw.12306.cn"]

    def __init__(self):
        with open('ips1.txt', 'r') as a:
            self.ips = a.readlines()[0].split(',')
        self.today = datetime.datetime.now().strftime('%Y-%m-%d')
        self.data = '2017-08-30'
        self.from_location = '韶关'
        self.to_location = '深圳'
        # # 1：商务/特等，2：一等，3：二等
        self.zuowei = '3'
        self.checi = 'G73'
        # self.che_ci = [x for x in self.checi.split(',')]
        station_dict = station()
        self.from_station = station_dict[self.from_location.decode('utf-8')]
        self.to_station = station_dict[self.to_location.decode('utf-8')]
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
            'Host': 'kyfw.12306.cn'}

    def start_requests(self):
        while 1:
            url = 'https://' + random.choice(self.ips) + '/otn/leftTicket/query?leftTicketDTO.train_date=' + self.data + '&leftTicketDTO.from_station=' + \
                  self.from_station + '&leftTicketDTO.to_station=' + self.to_station + '&purpose_codes=ADULT'
            yield scrapy.Request(url=url, headers=self.headers, callback=self.parse, meta={'url': url},dont_filter=True)
            time.sleep(0.1)

    def parse(self, response):
        train = json.loads(response.body)['data']['result']
        for x in train:
            temp_list = x.split('|')
            erdeng = temp_list[30]
            yideng = temp_list[31]
            tedeng = temp_list[32]
            seat = {'1': tedeng, '2': yideng, '3': erdeng}
            if temp_list[3] in self.checi and seat[self.zuowei] > 0 and seat[self.zuowei] != u'无':
                print temp_list[3],seat[self.zuowei]
                img_code = code()
                yanzheng_post(img_code)
                zhengshi_login()
                ready_post(temp_list[0], self.data, self.today, self.from_station,self.to_station)
                time.sleep(0.5)
                SubmitToken, key_check_isChange = init()
                print SubmitToken, key_check_isChange
                people_comfir(SubmitToken)
                paidui(SubmitToken, temp_list[2], self.checi, temp_list[6], temp_list[7], temp_list[12], temp_list[15])
                comfir_buy(SubmitToken, key_check_isChange, temp_list[12], temp_list[15])
                id = final(SubmitToken)
                send_mail(id)
                os._exit(0)
        print u'无票',train[0]