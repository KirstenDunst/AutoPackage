"""
Author: Cao Shixin
Date: 2020-11-27 18:10:26
LastEditors: Cao Shixin
LastEditTime: 2020-12-04 14:47:02
Description: 发送消息
"""
import requests
import smtplib
import json
from email.mime.text import MIMEText
from email.header import Header
from email.utils import parseaddr, formataddr


class SendMessage:
    """
    发送消息处理
    """

    @staticmethod
    def format_address(s):
        name, address = parseaddr(s)
        return formataddr((Header(name, 'utf-8').encode(), address))

    @staticmethod
    def send_email(from_address, smtp_server, password, to_address):
        # https://www.pgyer.com/XXX app地址
        # 只是单纯的发了一个文本邮箱,具体的发附件和图片大家可以自己去补充
        msg = MIMEText(
            'Hello' + '╮(╯_╰)╭应用已更新,请下载测试╮(╯_╰)╭' +
            '蒲公英的更新会有延迟,具体版本时间以邮件时间为准' + '', 'html', 'utf-8')
        msg['From'] = SendMessage.format_address('iOS开发团队 <%s>' % from_address)
        msg['Subject'] = Header('来自iOS开发团队的问候……', 'utf-8').encode()
        server = smtplib.SMTP(smtp_server, 25)  # SMTP协议默认端口是25
        server.set_debuglevel(1)
        server.login(from_address, password)
        server.sendmail(from_address, [to_address], msg.as_string())
        server.quit()
        print("===========邮件发送成功===========")

    @staticmethod
    def send_ding_talk_text(text, ding_talk_token):
        # 向钉钉群发送文本消息
        print(text)
        headers = {'Content-Type': 'application/json'}
        webhook = 'https://oapi.dingtalk.com/robot/send?access_token={}'.format(
            ding_talk_token)
        data = {
            "msgtype": "text",
            "text": {
                "content": text + '\n'
            },
            "at": {
                "atMobiles": [],
                "isAtAll": False
            }
        }
        x = requests.post(url=webhook, data=json.dumps(data), headers=headers)
        return x.reason

    @staticmethod
    def send_ding_talk_link(url):
        # 向钉钉群发送链接消息
        headers = {'Content-Type': 'application/json;charset=utf-8'}
        data = {
            "msgtype": "link",
            "link": {
                "text": '点我跳转百度',
                "title": "点我",
                "picUrl": "图片链接",  # 可以加，可以不加
                "messageUrl": "https://www.baidu.com"
            },
        }
        r = requests.post(url, data=json.dumps(data), headers=headers)
        return r.reason
