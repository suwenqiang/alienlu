#-*-coding:UTF-8-*-
from js import gethtml,parse
import datetime
import time
import requests
from bs4 import BeautifulSoup
from requests.packages.urllib3.exceptions import InsecureRequestWarning


requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36'}
urls = []
print datetime.datetime.now()
url = 'https://www.aliexpress.com/wholesale?site=glo&g=y&SortType=total_tranpro_desc&SearchText=18650&groupsort=1&page=1&initiative_id=AS_20170228225822&needQuery=n'
html = requests.get(url=url,headers=headers,verify=False).content
soup = BeautifulSoup(html,"html.parser")
titles = soup.findAll('a', attrs={'class':'picRind history-item '})
for item in titles:
    link = 'https://' + str(item['href'])
    urls.append(link)
print 'starting'
with open('a.csv','w') as a:
    x = 0
    for url in urls:
        gethtml(url=url,file_name=a)
        print x,u'parser over'
        print datetime.datetime.now()
        x = x + 1
        time.sleep(5)
        
print datetime.datetime.now()
