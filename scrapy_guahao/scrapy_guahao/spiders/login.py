#coding=UTF-8
import requests
import json
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
from lxml import etree

def guahao(id,cookies):
    s = requests.Session()
    headers = {'Host': 'weixin.91160.com',
               'Connection': 'keep-alive',
               'Origin': 'https://weixin.91160.com',
               'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 MicroMessenger/6.5.2.501 NetType/WIFI WindowsWechat QBCore/3.43.691.400 QQBrowser/9.0.2524.400',
               'Accept-Encoding': 'gzip, deflate',
               'Accept-Language': 'zh-CN,zh;q=0.8,en-us;q=0.6,en;q=0.5;q=0.4'}
    ##################登录#############################
    login_url = 'https://weixin.91160.com/user/login.html'
    data = {'username': '',
            'password': ''}
    s.post(url=login_url, headers=headers, cookies=cookies,data=data,verify=True)
    #print u'#################预约url处理######################'
    sch_url = 'https://weixin.91160.com/doctor/detlnew.html?' + \
               'unit_detl_map=[{%22unit_id%22:%22' + str(id['unit_id']) \
              +'%22,%22doctor_id%22:%22' + str(id['doctor_id']) + \
              '%22,%22dep_id%22:%22' + str(id['dep_id']) + \
              '%22,%22schedule_id%22:%22' + str(id['sch_id']) + '%22}]'
    sch_html = s.get(url=sch_url,headers=headers,cookies=cookies,verify=True)
    detl_id = json.loads(sch_html.content)['data'][id['sch_id']][0]['detl_id']
    #################token_url处理#####################
    token_url = 'https://weixin.91160.com/order/confirm.html?unit_id=' + id['unit_id'] + \
                '&sch_id=' + id['sch_id'] + \
                '&dep_id=' + id['dep_id'] + \
                '&detl_id=' + detl_id
    html= s.get(url=token_url,headers=headers,cookies=cookies,verify=True)
    selector = etree.HTML(html.content)
    token_key = selector.xpath('*//input[@name="token_key"]//@value')[0]

    submit_url = 'https://weixin.91160.com/order/submit.html'
    submit_data = {'mobile': '',
                   'mid': '',
                   'insurance': '0',
                   'insurance_ztb': '1',
                   'casualty_zm': '0',
                   'is_use_order_service': '0',
                   'token_key': token_key}
    submit_html = s.post(url=submit_url,data=submit_data,cookies=cookies,headers=headers,verify=True)
    result = json.loads(submit_html.content)
    return result['state'], result['msg']