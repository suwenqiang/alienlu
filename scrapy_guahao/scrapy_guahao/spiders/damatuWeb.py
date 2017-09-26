#coding=utf-8
import datetime
import hashlib
import requests
# import urllib.request
import urllib
import json
import base64

def md5str(str): #md5加密字符串
		m=hashlib.md5(str.encode(encoding = "utf-8"))
		return m.hexdigest()
		
def md5(byte): #md5加密byte
		return hashlib.md5(byte).hexdigest()
		
class DamatuApi():
	
	ID = '50651'
	KEY = '93310cab071cbddd2cba4c3aa09ee563'
	HOST = 'http://api.dama2.com:7766/app/'
	
	
	def __init__(self,username,password):
		self.username=username
		self.password=password
		
	def getSign(self,param=b''):
		return (md5(bytes(self.KEY) + bytes(self.username) + param))[:8]
		
	def getPwd(self):
		return md5str(self.KEY +md5str(md5str(self.username) + md5str(self.password)))
		
	def post(self,path,params={}):
		data = urllib.urlencode(params).encode('utf-8')
		url = self.HOST + path
		return requests.get(url,data).content
    
	#上传验证码 参数filePath 验证码图片路径 如d:/1.jpg type是类型，查看http://wiki.dama2.com/index.php?n=ApiDoc.Pricedesc  return 是答案为成功 如果为负数 则为错误码
	def decode(self,filePath,type):
		f=open(filePath,'rb')
		fdata=f.read()
		filedata=base64.b64encode(fdata)
		f.close()
		data={'appID':self.ID,
			'user':self.username,
			'pwd':dmt.getPwd(),
			'type':type,
			'fileDataBase64':filedata,
			'sign':dmt.getSign(fdata)
		}		
		res = self.post('d2File',data)
		res = str(res)
		jres = json.loads(res)
		if jres['ret'] == 0:
			#注意这个json里面有ret，id，result，cookie，根据自己的需要获取
			return(jres['result'])
		else:
			return jres['ret']
		
# #调用类型实例：
# #1.实例化类型 参数是打码兔用户账号和密码
dmt=DamatuApi("alienlu","hayabusa1340")
# #2.调用方法：
# print datetime.datetime.now()
# print(dmt.decode('capcha.png',23)),datetime.datetime.now() #上传打码,


