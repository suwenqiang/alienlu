import requests
import re


def station():
    url = 'https://kyfw.12306.cn/otn/resources/js/framework/station_name.js?station_version=1.9023'
    response = requests.get(url, verify=False)
    stations = re.findall(u'([\u4e00-\u9fa5]+)\|([A-Z]+)', response.text)
    station_dict = dict(stations)
    return station_dict