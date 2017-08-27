#coding=utf-8
import requests
import json
import time
import datetime


idurl = 'https://api.nike.com/payment/preview_results/v2/'
checkoutid = requests.get(url=idurl).json()['error_id']
paymentid = requests.get(url=idurl).json()['error_id']

session = requests.session()
loginurl = 'https://unite.nike.com/loginWithSetCookie?appVersion=299&experienceVersion=264&uxid=com.nike.commerce.snkrs.web&locale=zh_CN&backendEnvironment=identity&browser=&os=Windows%20NT%2010.0%3B%20WOW64&mobile=false&native=false&visit=1&visitor=e48afb62-edee-421b-86a7-c78613ff1304 HTTP/1.1'

loginHeaders = {
	'host':'unite.nike.com',
	'Content-Type':'text/plain',
	'Origin':'https://www.nike.com',
	'Connection':'keep-alive',
	'Accept':'*/*',
	'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0',
	'Accept-Encoding':'gzip, deflate',
}
loginPayload={
	"username":"",
	"password":"",
	"client_id":"",
	"ux_id":"com.nike.commerce.snkrs.ios",
	"grant_type":"password",
	'keepMeLoggedIn':'true'
}

loginResp=session.post(loginurl,data=json.dumps(loginPayload),headers=loginHeaders)
access_token=str(loginResp.json()['access_token'])
print access_token

headers = {
           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0',
           'Accept': 'application/json',
           'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
           'Accept-Encoding': 'gzip, deflate, br',
           'Content-Type': 'application/json; charset=UTF-8',
           'Authorization': 'Bearer '+ str(access_token),
           'Origin': 'https://www.nike.com',
           'Connection': 'keep-alive'}



html0 = session.options(url='https://api.nike.com/buy/checkout_previews/v2/' + checkoutid,headers=headers)
print html0.status_code,html0.headers


post_data = {"request":{"email":"81140140@qq.com","country":"CN","currency":"CNY","locale":"zh_CN","channel":"SNKRS","clientInfo":{"deviceId":"0400R9HVeoYv1gsNf94lis1ztnqv7CRnBjGO6/Ao2WE9gwpcE7v8aPDcWlOv5uA0UdlgseU3hf6ZgJHVGVmGHhZkVg779SPfw9jg/bn+kus6mYbBOmoLto4X8btxUT7HF5Mfhlz5wlRFwWJi0FRulruXQQGCQaJkXU7G/xCx87H3fYLqtP6CELnsH2G/cdkIMFbm6Yf0/pTJUUzbuPzsQkRu5wydKgnOIDKXq4HnEqNOos1c6njJgQh/4uWPf9I5I43RRL7fOkkwV0dTsyiI82NHxcfuqPY9fpixLEzP4TAbNLx4B5Y+hlUTFU590nH6wX2EIJPl7taneAp+euwBRWG3oPxIPhWfkls2Dvmh2Ql/4ZmxrGle/ZqF1WSwCPCGIJ9ojofZbR2X0CLQi4PDljQGTZxyTYzWRQCIYmH70/9WYFgrFNC6lStdnvLrIbcVhbjA6CiAMtmPSSvD4TWhv78VEIne56x7fyVRlv/nuXQXQGvX0gKDOFP1a/PoP5g1QwsR6HPyNaJmTDai9XF2InkrPPEFszfR7TVeYTtUNo5lYHxObL5PzR66nFRQJiixP4LBaxBeNabCoO0mlBgAVSsOVyyofExHIwDdyG4AHEbU3IynXrhcnO4UgCiP3k08ruO2MV2HeXfsIpcBAz+JqnVObFzqeMmBCH/ieLkYYw7gRCdLh7h/QYTtLeSWd2Bz5ubbq4HnEqNOos1/ARf3yJm6ITKx4PQbX9OHEQi+wlGoZ8WFk9C8+4pEn8Th1HyH9FgHkp62yUjciLEbPmkId7X9UBOd0/ewrrCpRONsrNmlQ0HEpvsUb5+Jr8qK4pvupFpLCfh5mpkjbY8JuvK70bwBpMhq5G0JDAEfjhfTyMu2WPU60XI1EZKVyZnHyH/spdP176ZigQa7PSc/NzbdUf1XOt8yWPvgXmLrlec+amWueJGZ4qN4QLKvqUV6ETiAWTGOqSKmGE9zDPF+pgCd2Ux7tt1mhTHKQ7jy9YMNjqOzgRW6psCbeWacXO7lr/RXFLtCT3fKaEmHgdZTpQDsI1l5pRcWvEsMdd2+SxT8V+5FRjwlPEdtOvY8eD35tOUw6jrqNh+QxW8Z/i97IRumGgXkYUn43/pPHCmdlDbGqeGq16udizKgcTSmkq/0eVBwKCbFEPNOpFjI2/6EOwkchN4u2PRWt+WNpGvHIi7SoUevORpROJ9qSFv+eJR3sCFSNJMUA7mWm5ddG/uXwr835+t4m0pJOwycmYRLIEgMnyu7KEs="},
                        "items":[{"id":"b1700e8e-f7c0-5734-bf8a-e575c82b6ec0","skuId":"14b2c9c4-fabb-5c5b-936a-26498413e21c","quantity":1,"recipient":{"firstName":"俊杰","lastName":"杨"},"shippingAddress":{"address1":"大中华国际金融中心A栋","address2":"34","city":"深圳市","state":"CN-44","postalCode":"518000","county":"福田区","country":"CN"},"contactInfo":{"email":"81140140@qq.com","phoneNumber":"13569897885"},"shippingMethod":"GROUND_SERVICE"}]}}

html1 = session.put(url='https://api.nike.com/buy/checkout_previews/v2/' + checkoutid,headers=headers,data=json.dumps(post_data))
print html1.content
jobs =  html1.json()['links']["self"]["ref"]


html2 = session.get(url='https://api.nike.com' + jobs,headers=headers)
print html2.json()
pay_url = 'https://api.nike.com/payment/preview/v2/'
pay_data = {"checkoutId":checkoutid,"total":1399,"currency":"CNY","country":"CN",
            "items":[{"productId":"b1700e8e-f7c0-5734-bf8a-e575c82b6ec0",
                      "shippingAddress":{"address1":"大中华","address2":"34","city":"市","state":"CN-44","postalCode":"518000","county":"福田区","country":"CN"}}],"paymentInfo":[{"id":paymentid,"billingInfo":{"name":{"firstName":"俊杰","lastName":"杨"},"address":{"address1":"大中华国际金融中心A栋","city":"深圳市","state":"CN-44","postalCode":"518000","county":"福田区","country":"CN"},"contactInfo":{"phoneNumber":"+8618665971006","email":"81140140@qq.com"}},"type":"Alipay"}]}
pay_html = session.post(url=pay_url,headers=headers,data=json.dumps(pay_data))
print pay_html.json()
paymenpreview = pay_html.json()['links']['self']['ref']
paymenpreview_url = 'https://api.nike.com' + paymenpreview
paymenpreviewjobs = session.get(url=paymenpreview_url,headers=headers)
paymentToken = paymenpreviewjobs.json()['id']
print paymentToken
print paymenpreviewjobs.json()
session.options(url='https://api.nike.com' + '/payment/preview/v2/',headers=headers)

checkouts_url = 'https://api.nike.com/buy/checkouts/v2/' + checkoutid
checkouts_data = {"request":{"email":"81140140@qq.com",
                             "country":"CN","currency":"CNY","locale":"zh_CN",
                             "channel":"SNKRS",
                             "clientInfo":{"deviceId":"0400R9HVeoYv1gsNf94lis1ztnqv7CRnBjGO6/Ao2WE9gwpcE7v8aPDcWlOv5uA0UdlgseU3hf6ZgJHVGVmGHhZkVg779SPfw9jg/bn+kus6mYbBOmoLto4X8btxUT7HF5Mfhlz5wlRFwWJi0FRulruXQQGCQaJkXU7G/xCx87H3fYLqtP6CELnsH2G/cdkIMFbm6Yf0/pTJUUzbuPzsQkRu5wydKgnOIDKXq4HnEqNOos1c6njJgQh/4uWPf9I5I43RRL7fOkkwV0dTsyiI82NHxcfuqPY9fpixLEzP4TAbNLx4B5Y+hlUTFU590nH6wX2EIJPl7taneAp+euwBRWG3oPxIPhWfkls2Dvmh2Ql/4ZmxrGle/ZqF1WSwCPCGIJ9ojofZbR2X0CLQi4PDljQGTZxyTYzWRQCIYmH70/9WYFgrFNC6lStdnvLrIbcVhbjA6CiAMtmPSSvD4TWhv78VEIne56x7fyVRlv/nuXQXQGvX0gKDOFP1a/PoP5g1QwsR6HPyNaJmTDai9XF2InkrPPEFszfR7TVeYTtUNo5lYHxObL5PzR66nFRQJiixP4LBaxBeNabCoO0mlBgAVSsOVyyofExHIwDdyG4AHEbU3IynXrhcnO4UgCiP3k08ruO2MV2HeXfsIpcBAz+JqnVObFzqeMmBCH/ieLkYYw7gRCdLh7h/QYTtLeSWd2Bz5ubbq4HnEqNOos1/ARf3yJm6ITKx4PQbX9OHEQi+wlGoZ8WFk9C8+4pEn8Th1HyH9FgHkp62yUjciLEbPmkId7X9UBOd0/ewrrCpRONsrNmlQ0HEpvsUb5+Jr8qK4pvupFpLCfh5mpkjbY8JuvK70bwBpMhq5G0JDAEfjhfTyMu2WPU60XI1EZKVyZnHyH/spdP176ZigQa7PSc/NzbdUf1XOt8yWPvgXmLrlec+amWueJGZ4qN4QLKvqUV6ETiAWTGOqSKmGE9zDPF+pgCd2Ux7tt1mhTHKQ7jy9YMNjqOzgRW6psCbeWacXO7lr/RXFLtCT3fKaEmHgdZTpQDsI1l5pRcWvEsMdd2+SxT8V+5FRjwlPEdtOvY8eD35tOUw6jrqNh+QxW8Z/i97IRumGgXkYUn43/pPHCmdlDbGqeGq16udizKgcTSmkq/0eVBwKCbFEPNOpFjI2/6EOwkchN4u2PRWt+WNpGvHIi7SoUevORpROJ9qSFv+eJR3sCFSNJMUA7mWm5ddG/uXwr835+t4m0pJOwycmYRLIEgMnyu7KEs="},
                             "items":[{"id":"b1700e8e-f7c0-5734-bf8a-e575c82b6ec0","skuId":"14b2c9c4-fabb-5c5b-936a-26498413e21c","quantity":1,
                                       "recipient":{"firstName":"","lastName":""},"shippingAddress":{"address1":"","address2":"34","city":"","state":"CN-44","postalCode":"518000","county":"","country":"CN"},"contactInfo":{"email":"81140140@qq.com","phoneNumber":"13569897885"},"shippingMethod":"GROUND_SERVICE"}],
                             "paymentToken":paymentToken}}
checkouts_html = session.put(url=checkouts_url,data=json.dumps(checkouts_data),headers=headers)
print checkouts_html.json()
checkouts_jobs_url = 'https://api.nike.com' + checkouts_html.json()['links']['self']['ref']
print checkouts_jobs_url
session.options(url=checkouts_jobs_url,headers=headers)
time.sleep(5)
checkouts_jobs_html = session.get(url=checkouts_jobs_url,headers=headers)
print checkouts_jobs_html.content
order_id = checkouts_jobs_html.json()['response']['orderId']
paymentApprovalId = checkouts_jobs_html.json()['response']['paymentApprovalId']
print order_id,paymentApprovalId

payment_url = 'https://api.nike.com/payment/deferred_payment_forms/v1'
return_url = "https://www.nike.com/cn/launch/deferredPayment?nikeorderid=" + order_id + "&nikepaymentapprovalid=" + paymentApprovalId + "&nikepaymenttype=AliPay&nikestylecolor=414571-004"
paymentdata = {"request":{"approvalId":paymentApprovalId,"returnURL":return_url,"orderNumber":order_id,"experienceType":"DESKTOP"}}
payment_html = session.post(url=payment_url,data=json.dumps(paymentdata),headers=headers)
code_url = 'https://api.nike.com' + payment_html.json()['links']['self']['ref']
print code_url

code_html = session.get(url=code_url,headers=headers)
code_img = code_html.json()['response']['qrCodeURL']
print '支付宝二维码连接',code_img
print datetime.datetime.now()


