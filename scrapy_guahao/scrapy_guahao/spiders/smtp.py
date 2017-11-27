#!/usr/bin/python
#-*-coding:UTF-8-*-

import smtplib
import time
from email.mime.text import MIMEText
def send_mail(messages):
    date = time.strftime('%m-%d %H:%M')

    mail_host = 'smtp.qian88.com.cn'

    mail_user = ''
    mail_passwd = ''

    sender = ''
    receivers = []


    message = MIMEText(str(messages + '挂到了'))
    message['Subject'] = str(date)
    message['From'] = sender
    message['To'] = receivers[0]

    smtpObj = smtplib.SMTP(mail_host)
    smtpObj.login(mail_user,mail_passwd)
    smtpObj.sendmail(sender,receivers,message.as_string())
    smtpObj.quit()
    print str(date),'success'
