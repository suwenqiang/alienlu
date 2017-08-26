#coding=UTF-8
import requests
import json
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
from urllib import urlencode
from lxml import etree
import time
from yanzhengma import img
import os


def guahao(id):
    s = requests.Session()
    print u'#################登录#############################'
    login_url = 'https://wap.91160.com/user/login.html'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'}
    data = {'username': '',
            'password': ''}
    s.post(url=login_url, headers=headers, data=data, verify=False)
    print u'#################登录成功#########################'
    sch_url = 'https://wap.91160.com/doctor/detlnew.html?' + \
               'unit_detl_map=[{%22unit_id%22:%22' + str(id['unit_id']) \
              +'%22,%22doctor_id%22:%22' + str(id['doctor_id']) + \
              '%22,%22dep_id%22:%22' + str(id['dep_id']) + \
              '%22,%22schedule_id%22:%22' + str(id['sch_id']) + '%22}]'
    sch_html = s.get(url=sch_url,headers=headers)
    detl_id = json.loads(sch_html.content)['data'][id['sch_id']][1]['detl_id']
    token_url = 'https://wap.91160.com/order/confirm.html?unit_id=' + id['unit_id'] + \
                '&sch_id=' + id['sch_id'] + \
                '&dep_id=' + id['dep_id'] + \
                '&detl_id=' + detl_id
    html= s.get(url=token_url,headers=headers)
    selector = etree.HTML(html.content)
    token_key = selector.xpath('*//input[@name="token_key"]//@value')[0]
    print u'################验证码处理#########################'
    rand = int(time.time())*1000
    capcha_url = 'https://wap.91160.com/sys/captcha.html?rand=' + str(rand)
    capcha_html = requests.get(url=capcha_url,headers=headers).content
    with open('capcha.png','wb') as a:
        a.write(capcha_html)
    img_code = img('capcha.png')
    submit_url = 'https://wap.91160.com/order/submit.html'
    submit_data = {'mobile':'XXXX',
                   'mid':'XXXXX',
                   'rand':rand,
                   'captcha':img_code,
                   'insurance':'0',
                   'insurance_ztb':'1',
                   'casualty_zm':'0',
                   'is_use_order_service':'0',
                   'token_key':token_key}
    print u'################提交预约###########################'
    submit_html = s.post(url=submit_url,data=submit_data,headers=headers)
    result = json.loads(submit_html.content)
    print result['state'], result['msg']
    return result['state']
