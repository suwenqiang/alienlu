#!/usr/bin/python
#-*-coding:UTF-8-*-

import smtplib
import time
from email.mime.text import MIMEText
def send_mail(id):
    date = time.strftime('%m-%d %H:%M')

    mail_host = 'smtp.qian88.com.cn'

    mail_user = 'XXXXX.com.cn'
    mail_passwd = 'XXXXX)'

    sender = 'XXXXX'
    receivers = ['XXXXX@qq.com']


    message = MIMEText(str(id))
    message['Subject'] = str(date) + u'刷到了'
    message['From'] = sender
    message['To'] = receivers[0]

    smtpObj = smtplib.SMTP(mail_host)
    smtpObj.login(mail_user,mail_passwd)
    smtpObj.sendmail(sender,receivers,message.as_string())
    smtpObj.quit()
    print str(date),'success'
