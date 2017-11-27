# -*- coding: utf-8 -*-
import MySQLdb
import settings
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

MYSQL_HOSTS = settings.MYSQL_HOSTS
MYSQL_USER = settings.MYSQL_USER
MYSQL_PASSWORD = settings.MYSQL_PASSWORD
MYSQL_PORT = settings.MYSQL_PORT
MYSQL_DB = settings.MYSQL_DB

class BothaiPipeline(object):
    def __init__(self):
        self.conn = MySQLdb.connect(host=MYSQL_HOSTS, port=MYSQL_PORT, user=MYSQL_USER, passwd=MYSQL_PASSWORD,db=MYSQL_DB)
        self.cur = self.conn.cursor()

    def process_item(self, item, spider):
        try:
            self.cur.execute("insert into %s(Time,volume_usd,price_btc,price_usd,market_cap_by_available_supply) values('%s',%s,%s,%s,%s)" %
                             (item['coin'],item['Time'], item['volume_usd'],item['price_btc'],item['price_usd'],item['market_cap_by_available_supply'],))
            self.conn.commit()
        except:
            self.cur.execute("update %s set volume_usd=%s,price_btc=%s,price_usd=%s,market_cap_by_available_supply=%s where Time=%s" %
                             (item['coin'], item['volume_usd'],item['price_btc'],item['price_usd'], item['market_cap_by_available_supply'],item['Time'],))
            self.conn.commit()
    def close(self):
        self.cur.close()
        self.conn.close()

