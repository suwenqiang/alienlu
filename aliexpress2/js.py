#coding:UTF-8

import time
from selenium import webdriver
from bs4 import BeautifulSoup

def parse(source,filename):
    soup = BeautifulSoup(source,"html.parser")
    country = soup.findAll('div', attrs={'class': 'user-country'})
    bidtime = soup.findAll('div', attrs={'class': 'order-time'})
    for (c, b) in zip(country, bidtime):
        filename.write(c.get_text())
        filename.write(',')
        filename.write(b.get_text())
        filename.write('\n')

def gethtml(url,file_name):
    driver = webdriver.PhantomJS()
    driver.set_window_size(1024, 10000)
    driver.get(url=url)
    time.sleep(5)
    try:
        source = driver.page_source
        parse(source=source, filename=file_name)
        driver.find_elements_by_xpath("//div[@class='ui-pagination-navi util-left']/a[@href='javascript:void(0);']")[0].click()#2
        time.sleep(5)
        source = driver.page_source
        parse(source=source,filename=file_name)
        driver.find_elements_by_xpath("//div[@class='ui-pagination-navi util-left']/a[@href='javascript:void(0);']")[2].click()#3
        time.sleep(5)
        source = driver.page_source
        parse(source=source, filename=file_name)
        driver.find_elements_by_xpath("//div[@class='ui-pagination-navi util-left']/a[@href='javascript:void(0);']")[3].click()#4
        time.sleep(5)
        source = driver.page_source
        parse(source=source, filename=file_name)
        driver.find_elements_by_xpath("//div[@class='ui-pagination-navi util-left']/a[@href='javascript:void(0);']")[4].click()#5
        time.sleep(5)
        source = driver.page_source
        parse(source=source, filename=file_name)
        driver.find_elements_by_xpath("//div[@class='ui-pagination-navi util-left']/a[@href='javascript:void(0);']")[5].click()#6
        time.sleep(5)
        source = driver.page_source
        parse(source=source, filename=file_name)
        driver.find_elements_by_xpath("//div[@class='ui-pagination-navi util-left']/a[@href='javascript:void(0);']")[6].click()#7
        time.sleep(5)
        source = driver.page_source
        parse(source=source, filename=file_name)
        driver.find_elements_by_xpath("//div[@class='ui-pagination-navi util-left']/a[@href='javascript:void(0);']")[3].click()#8
        time.sleep(5)
        source = driver.page_source
        parse(source=source, filename=file_name)
        driver.find_elements_by_xpath("//div[@class='ui-pagination-navi util-left']/a[@href='javascript:void(0);']")[3].click()#9
        time.sleep(5)
        source = driver.page_source
        parse(source=source, filename=file_name)
        driver.find_elements_by_xpath("//div[@class='ui-pagination-navi util-left']/a[@href='javascript:void(0);']")[3].click()#10
        time.sleep(5)
        source = driver.page_source
        parse(source=source, filename=file_name)
        driver.find_elements_by_xpath("//div[@class='ui-pagination-navi util-left']/a[@href='javascript:void(0);']")[3].click()  # 11
        time.sleep(5)
        source = driver.page_source
        parse(source=source, filename=file_name)
        driver.find_elements_by_xpath("//div[@class='ui-pagination-navi util-left']/a[@href='javascript:void(0);']")[3].click()  # 12
        time.sleep(5)
        source = driver.page_source
        parse(source=source, filename=file_name)
        driver.find_elements_by_xpath("//div[@class='ui-pagination-navi util-left']/a[@href='javascript:void(0);']")[3].click()  # 13
        time.sleep(5)
        source = driver.page_source
        parse(source=source, filename=file_name)
        driver.find_elements_by_xpath("//div[@class='ui-pagination-navi util-left']/a[@href='javascript:void(0);']")[3].click()  # 14
        time.sleep(5)
        source = driver.page_source
        parse(source=source, filename=file_name)
        driver.find_elements_by_xpath("//div[@class='ui-pagination-navi util-left']/a[@href='javascript:void(0);']")[3].click()  # 15
        time.sleep(5)
        source = driver.page_source
        parse(source=source, filename=file_name)
        print 'ok'
        driver.quit()
    except:
        driver.quit()
