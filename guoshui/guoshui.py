# coding=utf8
import time
import json
import requests
from PIL import Image,ImageEnhance
from pytesser import image_file_to_string
from selenium import webdriver
import random




def code(image):
    im=Image.open('D:\\Users\\lujunjie\\Desktop\\guoshui\\code.jpg')
    imgry = im.resize((256,256),Image.BILINEAR).convert('L')  # 图像加强，二值化
    sharpness = ImageEnhance.Contrast(imgry)  # 对比度增强
    sharp_img = sharpness.enhance(4)
    sharp_img.save("D:\\Users\\lujunjie\\Desktop\\guoshui\\image_code.jpg")
    code = image_file_to_string('D:\\Users\\lujunjie\\Desktop\\guoshui\\image_code.jpg')
    return code

def login():
    s = requests.session()
    login_url = 'http://dzswj.szgs.gov.cn/api/auth/clientWt'
    code_url = 'http://dzswj.szgs.gov.cn/JPEGServlet?d=1511936389264'
    headers = {'Host':'dzswj.szgs.gov.cn',
               'Accept':'application/json, text/javascript, */*; q=0.01',
               'Accept-Language': 'zh-CN,zh;q=0.8',
               'Content-Type':'application/json; charset=UTF-8',
               'Referer':'http://dzswj.szgs.gov.cn/BsfwtWeb/apps/views/login/login.html',
                'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
                'x-form-id':'mobile-signin-form',
                'X-Requested-With':'XMLHttpRequest',
               'Origin':'http://dzswj.szgs.gov.cn'}
    with open('code.jpg','wb') as w:
        w.write(s.get(url=code_url,headers=headers).content)
    time_local = time.localtime(int(time.time()))
    Time = time.strftime("%Y-%m-%d %H:%M:%S", time_local)
    login_data = {"nsrsbh":"","nsrpwd":"","tagger":code('img.jpg').strip('\n'),"redirectURL":"","time":Time}
    result = s.post(url=login_url,headers=headers,data=json.dumps(login_data))
    if result.json()['success'] == True:
        cookies = {}
        for (k,v) in zip(s.cookies.keys(),s.cookies.values()):
            cookies[k]=v
        return cookies
#登陆后的COOKIES获取
while 1:
    cookies = login()
    if cookies:
        break
print u'已经获取登陆后的cookies'
print cookies
driver = webdriver.PhantomJS(executable_path='D:\\Users\\lujunjie\\Desktop\\phantomjs-2.1.1-windows\\bin\\phantomjs.exe')
try:
# 国税查询
    print u'进行国税查询'
    driver.viewportSize={'width':2200,'height':2000}
    driver.get('http://dzswj.szgs.gov.cn')
    driver.delete_all_cookies()
    driver.add_cookie({'domain':'.szgs.gov.cn','name':'DZSWJ_TGC','value':cookies['DZSWJ_TGC'],'path':'/','expires': None})
    driver.add_cookie({'name':'JSESSIONID','value':cookies['JSESSIONID'],'domain':'.szgs.gov.cn','path':'/','expires': None})
    driver.add_cookie({'name':'tgw_l7_route','value':cookies['tgw_l7_route'],'domain':'.szgs.gov.cn','path':'/','expiry': int(time.time())})
    driver.set_window_size(1200, 1680)
    driver.get('http://dzswj.szgs.gov.cn/BsfwtWeb/apps/views/sb/cxdy/sbcx.html')
    time.sleep(3)
    #1.3 纳税申报列表截图
    print u'正在纳税申报列表截图'
    start_date = driver.find_element_by_xpath('//*[@id="sbrqq$text"]')
    start_date.clear()
    start_date.send_keys('20171001')
    end_date = driver.find_element_by_xpath("//*[@id='sbrqz$text']")
    end_date.clear()
    end_date.send_keys('20171129')
    driver.find_element_by_xpath('//a[@id="stepnext"]').click()
    time.sleep(3)
    driver.save_screenshot(u'纳税申报列表截图.png')
    #纳税申报详细截图
    print u'正在纳税申报详细截图'
    driver.find_elements_by_xpath('//*[@id="mini-grid-table-bodysbqkGrid"]//a[text()="查询申报表"]')[0].click()
    time.sleep(5)
    driver.find_element_by_class_name("mini-tools-max").click()
    time.sleep(1)
    driver.save_screenshot(u'纳税申报详细截图.png')
    #缴款信息查询
    print u'正在缴款信息查询'
    driver.get('http://dzswj.szgs.gov.cn/BsfwtWeb/apps/views/sb/djsxx/jk_jsxxcx.html')
    ns_start_date = driver.find_element_by_xpath('//*[@id="sssqq$text"]')
    ns_start_date.clear()
    ns_start_date.send_keys('20170101')
    ns_end_date = driver.find_element_by_xpath("//*[@id='sssqz$text']")
    ns_end_date.clear()
    ns_end_date.send_keys('20171129')
    driver.find_element_by_xpath('//a[@id="stepnext"]').click()
    time.sleep(3)
    driver.save_screenshot(u'已缴款列表截图.png')
    #地税查询
    print u'地税查询'
    def ds_login(cookies):
        s = requests.session()
        headers = {'Accept': 'application/json, text/javascript, */*; q=0.01',
                   'Accept-Language': 'zh-CN,zh;q=0.8',
                   'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
                   'X-Requested-With':'XMLHttpRequest'}
        todo_url = 'http://dzswj.szgs.gov.cn/api/gs/toDs'
        html = s.post(url=todo_url,headers=headers,cookies=cookies)
        data = html.json()['data']
        ds_url = 'https://dzswj.szds.gov.cn/dzswj/qyUserLogin.do?method=qyLogin&flag=gs&gnmk=sfjn&Pzxh=&token=' + data
        return ds_url
    url = ds_login(cookies)
    driver.get(url)
    time.sleep(2)
    #已申报信息查询
    print u'已申报信息查询'
    driver.get('https://dzswj.szds.gov.cn/dzswj/sbxxcx.do?method=toSbxxCx&qyyhDzswjRandomNum=0.42272002992090396')
    driver.find_element_by_xpath('//div[@class="input-group input-daterange"]//span[@class="select2-selection__arrow"]').click()
    driver.find_element_by_xpath('//*[@value="10109"]').click()
    ds_start_date = driver.find_element_by_xpath('//*[@id="sbqq"]')
    ds_start_date.clear()
    ds_start_date.send_keys('2017-10-01')
    ds_end_date = driver.find_element_by_xpath("//*[@id='sbqz']")
    ds_end_date.clear()
    ds_end_date.send_keys('2017-11-29')
    time.sleep(5)
    driver.find_element_by_xpath('//*[@id="query"]').click()
    time.sleep(2)
    driver.save_screenshot(u'已申报信息.png')
    #pdf
    print u'保存PDF'
    id = driver.find_element_by_xpath('//tr[@data-index="0"]/td[2]').text
    driver.find_element_by_name('btSelectItem').click()
    time.sleep(5)
    driver.find_element_by_id('print').click()
    time.sleep(2)
    ck1 = driver.get_cookies()
    pdf_ck = {}
    for x in ck1:
        pdf_ck[x['name']]=x['value']
    pdf_url = driver.find_element_by_name('sbbFormCj').get_attribute('action')
    pzhx = driver.find_element_by_name('yzpzxhArray').get_attribute('value')
    pdf_data = {'SubmitTokenTokenId':'','yzpzxhArray':pzhx,'btSelectItem':'on'}
    headers = {'Accept': 'application/json, text/javascript, */*; q=0.01',
               'Accept-Language': 'zh-CN,zh;q=0.8',
               'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
               'X-Requested-With': 'XMLHttpRequest'}
    with open(u'已申报截图.pdf','wb') as w:
        w.write(requests.post(url=pdf_url,headers=headers,data=pdf_data,cookies=pdf_ck).content)
    #2.5地税缴款查询
    driver.get('https://dzswj.szds.gov.cn/dzswj/yjkxxcx.do?method=init&qyyhDzswjRandomNum=0.08405041267793534')
    ds_start_date = driver.find_element_by_xpath('//*[@id="jkqq"]')
    ds_start_date.clear()
    ds_start_date.send_keys('2017-07-01')
    ds_end_date = driver.find_element_by_xpath("//*[@id='jkqz']")
    ds_end_date.clear()
    ds_end_date.send_keys('2017-09-01')
    driver.find_element_by_xpath('//*[@id="query"]').click()
    time.sleep(2)
    driver.find_element_by_id('cxjkmx').click()
    jkpdf_id = driver.find_element_by_xpath('//tr[@data-index="0"]/td[2]').text
    #2.7
    print u'已缴款截图'
    with open(u'已缴款截图.html','wb') as x:
        x.write(requests.get(url='https://dzswj.szds.gov.cn/dzswj/yjkxxcx.do?method=queryDetail&xtsphm=' + jkpdf_id + '&dzswjRandonNum%20=' + str(random.randint(1000,9999)),headers=headers,cookies=pdf_ck).content)
    driver.quit()
except:
    driver.quit()