#coding=UTF-8
import requests
import json
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
from guahao import guahao
import datetime
import os
import time
import random


to_date = '2017-08-20'
time_type = 'am'
s = requests.Session()
headers ={'user-agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Mobile Safari/537.36'}
url_accont = 'https://wap.91160.com/doctor/schedule.html?unit_id=131&dep_id=769&doctor_id=18241'
def gua():
    while 1:
        html = s.get(url=url_accont,headers=headers)
        print
        id = {}
        print html.content
        for x in json.loads(html.content)['data']['sch']:
                if x['to_date'] == to_date and x['time_type'] == time_type and x['y_state'] == '1':
                    id['unit_id'] = x['unit_id']
                    id['doctor_id'] = x['doctor_id']
                    id['dep_id'] = x['dep_id']
                    id['sch_id'] = x['schedule_id']
                    print u'有号可以挂了',x['to_date'],x['time_type'],x['y_state']
                    result = guahao(id)
                    if result == -4:
                        print result
                        time.sleep(1)
                        gua()
                    os._exit(0)
        # random_time = random.randint(1,3)
        print u'无号',datetime.datetime.now(),json.loads(html.content)['data']['sch'][0]['y_state_desc']
        time.sleep(1)
gua()
