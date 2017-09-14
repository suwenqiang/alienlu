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
import re
import PyV8

s = requests.Session()
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
           'Host': 'wap.91160.com',
           'Upgrade-Insecure-Requests': '1',
           'Referer': 'https://wap.91160.com/'}

#获取动态js，添加cookies
url = 'https://wap.91160.com'
html = s.get(url=url,headers=headers)
print html.cookies.keys()[0],html.cookies.values()[0]
js_func_string = re.search(r'.*?<script>(.*?)</script>',html.content).group(1).replace('eval(y',"String(y")
ctxt = PyV8.JSContext()
ctxt.enter()
c = ctxt.eval("""{js}""".format(js=js_func_string))
part = re.search('\{\};(var.*?\+=cd;).*?',c).group(1)
d =  part + 'String(dc);'
e =  ctxt.eval("""{js}""".format(js=d))
cookie = {e.split('=')[0]:e.split('=')[1]}

#开始挂号
# to_date = '2017-08-20'
# time_type = 'am'
# url_accont = 'https://wap.91160.com/doctor/schedule.html?unit_id=131&dep_id=769&doctor_id=18241'
# def gua(cookies):
#     while 1:
#         html = s.get(url=url_accont,headers=headers,cookies=cookies)
#         id = {}
#         print html.content
#         for x in json.loads(html.content)['data']['sch']:
#                 if x['to_date'] == to_date and x['time_type'] == time_type and x['y_state'] == '1':
#                     id['unit_id'] = x['unit_id']
#                     id['doctor_id'] = x['doctor_id']
#                     id['dep_id'] = x['dep_id']
#                     id['sch_id'] = x['schedule_id']
#                     print u'有号可以挂了',x['to_date'],x['time_type'],x['y_state']
#                     result = guahao(id)
#                     if result == -4:
#                         print result
#                         time.sleep(1)
#                         gua(cookies)
#                     os._exit(0)
#         # random_time = random.randint(1,3)
#         print u'无号',datetime.datetime.now(),json.loads(html.content)['data']['sch'][0]['y_state_desc']
#         time.sleep(1)
# gua(cookie)
