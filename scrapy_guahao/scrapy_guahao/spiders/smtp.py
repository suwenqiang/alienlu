#!/usr/bin/python
#-*-coding:UTF-8-*-

import smtplib
import time
from email.mime.text import MIMEText
def send_mail():
    date = time.strftime('%m-%d %H:%M')

    mail_host = ''

    mail_user = 'XXX'
    mail_passwd = 'XXXX'

    sender = 'XXXXX'
    receivers = ['XXXX@qq.com']


    message = MIMEText(u'挂到了')
    message['Subject'] = str(date) + u'挂到了'
    message['From'] = sender
    message['To'] = receivers[0]

    smtpObj = smtplib.SMTP(mail_host)
    smtpObj.login(mail_user,mail_passwd)
    smtpObj.sendmail(sender,receivers,message.as_string())
    smtpObj.quit()
    print str(date),'success'