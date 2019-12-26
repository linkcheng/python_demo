#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import logging
import os.path
import smtplib
import traceback
from email import encoders
from email.header import Header
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

logger = logging.getLogger(__name__)


def send_mail(subj, cnt, to_addrs, from_addr, password, atts, smtp_addr='smtp.exmail.qq.com', smtp_port=465):
    """
    发送邮件
    :param subj: 邮件主题
    :param cnt: 邮件内容
    :param to_addrs: 收信人的邮箱地址
    :param from_addr: 发信人的邮箱地址
    :param password: 发信人的邮箱密码
    :param atts: 邮件附件 path list, []
    :param smtp_addr: SMTP server 地址
    :param smtp_port: SMTP server port
    :return:
    """

    if not isinstance(to_addrs, (tuple, list)):
        to_addrs = [to_addrs]

    if not isinstance(atts, (tuple, list)):
        atts = [atts]

    msg = MIMEMultipart()

    msg['Subject'] = Header(subj, 'utf-8')
    msg['From'] = from_addr
    msg['To'] = ','.join(to_addrs)

    # 邮件正文
    msg.attach(MIMEText(cnt, 'html', 'utf-8'))

    # 邮件附件
    for index, att in enumerate(atts):
        read_att_content(msg, att, index)

    try:
        server = smtplib.SMTP_SSL(smtp_addr, smtp_port)
        server.login(from_addr, password)
        server.sendmail(from_addr, to_addrs, msg.as_string())
        server.quit()
    except Exception as e:
        logger.error('Error: unable to send email')
        logger.error(traceback.format_exc())


def read_att_content(msg, att_path, index):
    # 跳过空文
    file_size = os.path.getsize(att_path)
    if file_size <= 0:
        return

    # 添加附件就是加上一个MIMEBase，从本地读取一个图片:
    with open(att_path, 'rb') as f:
        filename = att_path.split('/')[-1]
        # 设置附件的MIME和文件
        mime = MIMEBase('text', 'plain', filename=filename)
        # 加上必要的头信息:
        mime.add_header('Content-Disposition', 'attachment', filename=filename)
        mime.add_header('Content-ID', '<'+str(index)+'>')
        mime.add_header('X-Attachment-Id', str(index))
        # 把附件的内容读进来:
        mime.set_payload(f.read())
        # 用Base64编码:
        encoders.encode_base64(mime)
        # 添加到MIMEMultipart:
        msg.attach(mime)


if __name__ == '__main__':
    fromaddr = '*******@sfy.com'
    toaddrs = ['*******@qq.com']
    subject = u'测试邮件'
    password = '*******'
    content = u'测试一下'
    send_mail(subject, content, toaddrs, fromaddr, password)
