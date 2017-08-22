import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

#
# now = []
# nowork = []
# headers = {
#             'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
#             'Host': 'kyfw.12306.cn'}
# with open('ips.txt','r') as a:
#     for x in a.readlines():
#         now.append(x)
#         try:
#             url = 'https://' + x.strip('\n') + '/otn/leftTicket/query?leftTicketDTO.train_date=2017-08-18&leftTicketDTO.from_station=SNQ&leftTicketDTO.to_station=IOQ&purpose_codes=ADULT'
#             html = requests.get(url=url,headers=headers,verify=False,timeout=3)
#             if html.status_code != 200:
#                nowork.append(x.strip('\n'))
#             else:
#                 None
#         except:
#             nowork.append(x.strip('\n'))
# print len(now),len(nowork)
# for x in now:
#     if x.strip('\n') in nowork:
#         now.remove(x)
# print len(now)
# with open('ips2.txt','w') as b:
#     for y in now:
#         b.write(y.strip('\n'))
#         b.write(',')
