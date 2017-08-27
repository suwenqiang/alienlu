# -*- coding: utf-8 -*-
# 程序基本框架
import re
import requests
import json
from bs4 import BeautifulSoup
import urllib
import time
import sys
reload(sys)
sys.setdefaultencoding('utf8')

session=requests.Session()


# 商品页面
spurl='https://www.apple.com/cn/shop/buy-iphone/iphone-7/4.7-%E8%8B%B1%E5%AF%B8%E5%B1%8F%E5%B9%95-128gb-%E7%8E%AB%E7%91%B0%E9%87%91%E8%89%B2#00,14,21'
head={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.125 Safari/537.36',
    	  'Referer':'https://www.apple.com/cn/'}

res=session.get(spurl,headers=head)
#print res.text

soup=BeautifulSoup(res.text,'html.parser')
product=str(soup.select('script')).split('"sku":"')[1].split('"}]')[0]
#print product

script=str(soup.select('script')).split('window.asBuyFlow.reselectData = ')[1].split(';')[0]
infoDict=eval(script)
#print infoDict

size=infoDict['dimensionScreensize']
color=infoDict['dimensionColor']
capacity=infoDict['dimensionCapacity']
print size,color,capacity

#加入购物车
postUrl=spurl.split('#')[0]
data={  'product':product,
        'purchaseOption':'fullPrice',
        'step':'select',
        'complete':'true',
        'dimensionCapacity':capacity,
        'dimensionColor':color,
        'dimensionScreensize':size,
        'add-to-cart':'add-to-cart'}
data=urllib.urlencode(data)
add_cart=session.get(postUrl,headers=head,params=data)
print add_cart.status_code
print add_cart.url
#print add_cart.text

# 查看购物袋
cartUrl = 'https://www.apple.com/cn/shop/buy-iphone/'+spurl.split('/')[-2]+'?proceed=proceed&product='+product+'%2FA&step=attach'
cartHead = {'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Referer':add_cart.url,
            'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.125 Safari/537.36'}
cartResp = session.get(cartUrl,headers=head)
print cartResp.url
# print cartResp.text

#确定已加入购物车
URL = 'https://www.apple.com/cn/shop/bag/flyout'
data = {'apikey':'SJHJUH4YFCTTPD4F4',
        'l':add_cart.url+'#'}
resp = session.get(URL,headers=head,params=data)
# print resp.text


# 进入登陆页面

x_aos_stk = str(cartResp.text.split('x-aos-stk":"')[1].split('"}}')[0])
#loginPageUrl='https://secure2.store.apple.com/cn/shop/sign_in?c=aHR0cHM6Ly93d3cuYXBwbGUuY29tL2NuL3Nob3AvYmFnfDFhb3M0MzYxMjI5OWRhYjE0YWM3OThkYzk4NTMyZjE1MWUzZTZhMTMzMThj&o=O01MNksy&r=SXYD4UDAPXU7P7KXF&s=aHR0cHM6Ly9zZWN1cmUyLnN0b3JlLmFwcGxlLmNvbS9jbi9zaG9wL2NoZWNrb3V0L3N0YXJ0P3BsdG49MUYzOEExRjF8MWFvc2JhNTc2M2I4NzNhYzQ3ZWU5Y2IzYzY2ZGZkYzc4OWVhNjE1NWM0OWU&t=SXYD4UDAPXU7P7KXF&up=t'
getUrl = 'https://www.apple.com/cn/shop/bagx/checkout_now?_a=checkout&_m=shoppingCart'
getHead = { 'Referer':'https://www.apple.com/cn/shop/bag',
            'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.125 Safari/537.36',
            'X-Requested-With':'XMLHttpRequest',
            'x-aos-stk':x_aos_stk,
            'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8'
            }

id = re.search(r'"cart-items-item-(.*?)".*?',cartResp.text).group(1)
print id


data = urllib.urlencode({'shoppingCart.cart-items-item-'+id+'.quantity':'1',
        'shoppingCart.actions.fcscounter':'',
        'shoppingCart.actions.fcsdata':''})

getResp = session.post(getUrl,headers=getHead,data=data)
print getResp.text

loginPageUrl= json.loads(getResp.text)['head']['data']['url']
s = re.search(r'.*?=SXYD4UDAPXU7P7KXF&s=(.*?)&t=SXYD4UDAPXU7P7KXF&up=t',loginPageUrl).group(1)

# ##访客登陆
sign_inUrl = 'https://secure2.store.apple.com/cn/shop/sentryx/sign_in'
sign_inHead = { 'X-Requested-With':'XMLHttpRequest',
                'Content-Type':'application/x-www-form-urlencoded',
                'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.125 Safari/537.36'}

aywysya = 'cla44j1d7lY5BNvcKyAdMUDFBpBeA0fUm0NUbNiqNxp37H01yjaY2.rIN4WySXvOxwawgCgIlNu1k.QkCoq0NUuAuyPB94UXuGlfUm0NUbNiqUU8jA2Q3wLDVg.3IqupyNCiEzIlnXRcW1F7T9qQtEwJ3skRq4zUVRE_xUC54b_H_jXgqNBLyOtJJIqSI6KUMnGWpwoNSUC56MnGW87gq1HACVdcJWBKJd_9CUfSHolk2dUf.j7J1gBZEMgzH_y3Cmx_B4WugMJPqDxmejV2pNk0ug97HbSI_8yg1wWXKWZWuxbuXjmaicCmx_B4WBkl1BQLz4mvmfTT9oaSumKkpjlRiwerbXh8bUuYLzQW5BNv__5BNlVnIQkFY5DjV.7QH'
data = {
        'fdcBrowserData':'%7B%22U%22%3A%22Mozilla%2F5.0%20(Windows%20NT%206.1%3B%20WOW64)%20AppleWebKit%2F537.36%20(KHTML%2C%20like%20Gecko)%20Chrome%2F44.0.2403.125%20Safari%2F537.36%22%2C%22L%22%3A%22zh-CN%22%2C%22Z%22%3A%22GMT%2B08%3A00%22%2C%22V%22%3A%221.0%22%7D',
        '_a':'login.guestSign',
        'c':'aHR0cHM6Ly93d3cuYXBwbGUuY29tL2NuL3Nob3AvYmFnfDFhb3M0MzYxMjI5OWRhYjE0YWM3OThkYzk4NTMyZjE1MWUzZTZhMTMzMThj',
        '_fid':'si',
        'r':'SXYD4UDAPXU7P7KXF',
        's':s,
        't':'SXYD4UDAPXU7P7KXF',
        'up':'true'}

data=urllib.urlencode(data)
sign_inResp= session.post(sign_inUrl,headers=sign_inHead,data=data)
print sign_inResp.text
pltn = json.loads(sign_inResp.text)['head']['data']['args']['pltn']
print pltn

# # 问题点
startUrl = json.loads(sign_inResp.text)['head']['data']['url']
startHead = {   'Content-Type':'application/x-www-form-urlencoded',
                'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.125 Safari/537.36'}

data=urllib.urlencode({'pltn':pltn})
startResp = session.post(startUrl,headers=startHead,data=data)
# print startResp.text


# <input name="sessionID" type="hidden" value="699a71a3c803e6cb973c191b510c8e9bfac8f6802d85275e631bffb1b454a3b3" />
# Regx = re.sea(r'.*?name="sessionID".*?value=(.*?)\/>')
sessionId = re.search(r'.*?name="sessionID".*?value="(.*?)".*?',startResp.text).group(1)
print sessionId


checkoutUrl = 'https://secure2.store.apple.com/cn/shop/checkout'

data = {'pltn':pltn,
        'v':'on',
        'sessionID':sessionId}

data = urllib.urlencode(data)
checkoutResp = session.post(checkoutUrl,headers=startHead,data=data)
#print checkoutResp.text

#检查商品继续
id = str(checkoutResp.text.split('{"fields":[{"id":"')[1].split('",')[0])
print type(id),id

checkoutxUrl='https://secure2.store.apple.com/cn/shop/checkoutx'
data = {'sessionID':sessionId,
        id:'A8',
        '_a':'cart.cont',
        '_fid':'co',
        '_m':'cart'}
checkoutxHead = {'Content-Type':'application/x-www-form-urlencoded',
                 'Referer':'https://secure2.store.apple.com/cn/shop/checkout',
                 'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.125 Safari/537.36',
                 'X-Requested-With':'XMLHttpRequest'}

data = urllib.urlencode(data)
# data = 'sessionID='+sessionId+'&'+id+'=A8&_a=cart.cont&_fid=co&_m=cart'
checkoutxResp = session.post(checkoutxUrl,headers=checkoutxHead,data=data)
#print checkoutxResp.text
time.sleep(5)


print u'填写收货信息'
data = {'sessionID':sessionId,
        'shipping-user-lastName':'卢',
        'shipping-user-firstName':'胜',
        'shipping-user-daytimePhoneAreaCode':'027',
        'shipping-user-daytimePhone':'18665971006',
        'shipping-user-state':'湖北',
        'shipping-user-city':'武汉',
        'shipping-user-district':'汉阳区',
        'shipping-user-street':'汉阳造',
        'shipping-user-street2':'59栋',
        'shipping-user-postalCode':'432000',
        'shipping-user-emailAddress':'81140140@qq.com',
        'shipping-user-mobilePhone':'',
        'state':'湖北',
        'keyPath':'shipping.address',
        'city':'武汉',
        '_a':'ship.cont',
        '_fid':'co'}

data = urllib.urlencode(data)
addressResp = session.post(checkoutxUrl,headers=checkoutxHead,data=data)
#print addressResp.text
time.sleep(5)

print u'选择支付方式'
data = {'sessionID':sessionId,
        'undefined':'',
        'bankOption':'WeChat',
        '_a':'bill.cont',
        '_fid':'co'}

data = urllib.urlencode(data)
paytypeResp = session.post(checkoutxUrl,headers=checkoutxHead,data=data)
#print paytypeResp.text
time.sleep(5)

print u'发票'
data = {'sessionID':sessionId,
        'invoice-user-invoiceEmailAddress-emailAddress':'81140140@qq.com',
        'invoice-form-options-selection':'none',
        '_a':'invoice.cont',
        '_fid':'co'}

data = urllib.urlencode(data)
fapiao_Resp = session.post(checkoutxUrl,headers=checkoutxHead,data=data)


print fapiao_Resp.text
time.sleep(5)
print u'账户'
data = {'account-appleId':'',
        'account-password':'',
        'account-passwordAgain':'',
        'account-commsPref':'true',
        '_a':'acct.cont',
        '_fid':'co'}


data = urllib.urlencode(data)
account_Resp = session.post(checkoutxUrl,headers=checkoutxHead,data=data)
#print account_Resp.text
time.sleep(5)

print u'条款与条件'
data = {'sessionID':sessionId,
        'accept':'true',
        'acceptAppleTnc':'false',
        '_a':'terms.cont',
        '_fid':'co'}

data = urllib.urlencode(data)
item_Resp = session.post(checkoutxUrl,headers=checkoutxHead,data=data)
# print item_Resp.text
time.sleep(5)


print u'立即下单'
data = {
        'sessionID':sessionId,
        'promo-code':'',
        '_a':'po',
        '_fid':'co'}

data = urllib.urlencode(data)
xiadan_Resp = session.post(checkoutxUrl,headers=checkoutxHead,data=data)
print xiadan_Resp.text


#chexkout status
statusUrl = 'https://secure2.store.apple.com/cn/shop/checkout/status'

statushead = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.125 Safari/537.36',}

status_Resp = session.get(statusUrl,headers=statushead)
print status_Resp.status_code
# print status_Resp.text
time.sleep(5)


statusHead = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.125 Safari/537.36',
              'Content-Type': 'application/x-www-form-urlencoded'}
statusxUrl = 'https://secure2.store.apple.com/cn/shop/checkoutx'
data = {'_a':'status',
        '_fid':'co',
        '_m':'common'}

data = urllib.urlencode(data)
status = session.post(statusxUrl,headers=statusHead,data=data)
print status.text



print u'进入订单页'
paypageUrl = 'https://secure2.store.apple.com/cn/shop/checkout/thankyou'
paypage_Resp = session.get(paypageUrl,headers=head)

print paypage_Resp.text
print paypage_Resp.url
print paypage_Resp.status_code

# 获取支付链接信息
getPayurl = 'https://secure2.store.apple.com/cn/shop/checkoutx/thankyou'
data =urllib.urlencode ({'_a':'paynow','_fid':'co'})

getPayResp = session.post(getPayurl,headers=checkoutxHead)
print getResp.text
