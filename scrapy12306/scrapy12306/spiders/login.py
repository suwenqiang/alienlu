#coding=utf-8
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import  requests
import json
import re
import time
from yanzhengma import img
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


s = requests.Session()
headers ={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
          'Referer':'https://kyfw.12306.cn/otn/passport?redirect=/otn/login'}

headers_1 = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
            'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8'}

headers_3 = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
             'Content-Type': 'application/x-www-form-urlencoded'}

headers_4 = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'}

def code():
    print u'################获取验证码图片##################'
    img_url = 'https://kyfw.12306.cn/passport/captcha/captcha-image?login_site=E&module=login&rand=sjrand&0.4962595043288218'
    code = s.get(url=img_url,headers=headers,verify=False)
    with open('captcha.jpg','wb') as p:
        p.write(code.content)
    img_code = img('captcha.jpg')
    return img_code

def yanzheng_post(img_code):
    img_data = {'answer':img_code,'login_site':'E','rand':'sjrand'}
    print u'###############验证码识别完成，正在提交#########'
    code_url = 'https://kyfw.12306.cn/passport/captcha/captcha-check'
    headers_1 ={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
                'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8'}
    code = s.post(url=code_url,data=img_data,headers=headers_1,verify=False)
    print u'################验证码提交结果##################'
    print json.loads(code.content)['result_message']


def zhengshi_login():
    print u'################验证登录12306###################'
    login_url = 'https://kyfw.12306.cn/passport/web/login'
    login_data = {'username':'XXX@qq.com','password':'XXX','appid':'otn'}
    login_html = s.post(url=login_url,data=login_data,headers=headers_1,verify=False)
    print json.loads(login_html.content)['result_message']
    print u'###################正式登录#####################'
    login_url1 = 'https://kyfw.12306.cn/passport/web/auth/uamtk'
    login_data1 = {'appid':'otn'}
    login_html1 = s.post(url=login_url1,data=login_data1,verify=False,headers=headers_1)
    tk = json.loads(login_html1.content)['newapptk']
    login_data2 = {'tk':tk,'_json_att':''}
    login_url2 = 'https://kyfw.12306.cn/otn/uamauthclient'
    login_html2 = s.post(url=login_url2,data=login_data2,headers=headers_1,verify=False)
    print json.loads(login_html2.content)['result_message']

def ready_post(secertstr,train_date,back_train_date,query_from_station_name,query_to_station_name):
    print u'##################订单验证登录##################'
    check_user = 'https://kyfw.12306.cn/otn/login/checkUser?_json_att='
    check_user_html = s.post(url=check_user,headers=headers_1,verify=False)
    print json.loads(check_user_html.content)['data']
    print u'##################预订单POST###################'
    post_url = 'https://kyfw.12306.cn/otn/leftTicket/submitOrderRequest?secretStr='+\
               str(secertstr)+'&train_date=' + str(train_date) + '&back_train_date=' + back_train_date+ '&tour_flag=dc&purpose_codes=ADULT&query_from_station_name=' + str(query_from_station_name) + \
               '&query_to_station_name=' + str(query_to_station_name) + '&undefined='
    post_html = s.post(url=post_url,headers=headers_1,verify=False)
    print json.loads(post_html.content)

def init():
    print u'##################跳转initDc####################'
    dc_url = 'https://kyfw.12306.cn/otn/confirmPassenger/initDc?_json_att='
    dc_html = s.post(url=dc_url,headers=headers_3,verify=False).content
    SubmitToken = re.search(r'.*?var globalRepeatSubmitToken = \'(.*?)\';',dc_html).group(1)
    key_check_isChange = re.search(r".*?\'key_check_isChange\'\:\'(.*?)\'",dc_html).group(1)
    return SubmitToken,key_check_isChange

def people_comfir(SubmitToken):
    print u'#################常用联系人确定##################'
    lianxiren_url = 'https://kyfw.12306.cn/otn/confirmPassenger/getPassengerDTOs?_json_att=&REPEAT_SUBMIT_TOKEN=' + str(SubmitToken)
    lianxir_list = s.post(url=lianxiren_url,headers=headers_1)
    print json.loads(lianxir_list.content)['data']['normal_passengers']
    print u'#################购票人确定#####################'
    checkorder = 'https://kyfw.12306.cn/otn/confirmPassenger/checkOrderInfo'
    checkorder_data = {'cancel_flag':'2',
                       'bed_level_order_num':'000000000000000000000000000000',
                       'passengerTicketStr':'O,0,1,XXX,1,XXXX,XXXX,N',
                       'oldPassengerStr':'XXX,1,XXX,1_',
                       'tour_flag':'dc',
                       'randCode':'',
                       '_json_att':'',
                       'REPEAT_SUBMIT_TOKEN':SubmitToken}
    checkorder_response = s.post(url=checkorder,data=checkorder_data,headers=headers_1,verify=False)
    print json.loads(checkorder_response.content)['data']

def paidui(SubmitToken,train_no,checi,from_stationcode,to_stationcode,yp_info,train_location):
    print u'#################进入排队#######################'
    queue_url = 'https://kyfw.12306.cn/otn/confirmPassenger/getQueueCount'
    queue_data = {'train_date':'Tue Aug 25 2017 00:00:00 GMT+0800 (China Standard Time)',
                  'train_no':train_no,
                  'stationTrainCode':checi,
                  'seatType':'3',
                  'fromStationTelecode':from_stationcode,
                  'toStationTelecode':to_stationcode,
                  'leftTicket':yp_info,
                  'purpose_codes':'00',
                  'train_location':train_location,
                  '_json_att':'',
                  'REPEAT_SUBMIT_TOKEN':SubmitToken}
    queue_html = s.post(url=queue_url,data=queue_data,headers=headers_1,verify=False)
    print u'当前票数',json.loads(queue_html.content)['data']['ticket']
    print u'当前排队人数', json.loads(queue_html.content)['data']['countT']

def comfir_buy(SubmitToken,key_check_isChange,yp_info,train_location):
    print u'################确认购买########################'
    confirm_url = 'https://kyfw.12306.cn/otn/confirmPassenger/confirmSingleForQueue'
    confirm_data = {'passengerTicketStr':'O,0,1,XXX,1,XXXX,XXX,N',
                   'oldPassengerStr': 'XX,1,XXXX,1_',
                   'randCode':'',
                   'purpose_codes': '00',
                   'key_check_isChange':key_check_isChange,
                   'leftTicketStr':yp_info,
                   'train_location': train_location,
                   'choose_seats':'',
                   'seatDetailType':'000',
                   'roomType':'00',
                   'dwAll': 'N',
                   '_json_att':'',
                   'REPEAT_SUBMIT_TOKEN':SubmitToken}
    confirm_html = s.post(url=confirm_url,data=confirm_data,headers=headers_1,verify=False)
    print u'提交状态',json.loads(confirm_html.content)['data']['submitStatus']
def final(SubmitToken):
    print u'#################最后提交########################'
    randomtime = int(round(time.time() * 1000))
    final_url = 'https://kyfw.12306.cn/otn/confirmPassenger/queryOrderWaitTime?random=' + str(randomtime) + '&tourFlag=dc&_json_att=&REPEAT_SUBMIT_TOKEN=' + str(SubmitToken)
    result = s.post(url=final_url,headers=headers,verify=False)
    print json.loads(result.content)['data']['orderId']
    print u'订单号',json.loads(result.content)['data']['orderId']
    return str(json.loads(result.content)['data'])
