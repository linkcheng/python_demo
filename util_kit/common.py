#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import os
import os.path
import logging
import datetime
from collections import deque
from cache import Cache, cache
from mail import send_mail
from tool import str_fmt

logger = logging.getLogger(__name__)
mapper_id_cache = Cache('mapper_id_cache')
# 线程安全队列
transfer_log_deque = deque()
# 邮件附件目录
base_att_path = '/tmp/att'


def get_mapper_id(*args):
    return int(get_mapper_id_str(*args))


@cache(mapper_id_cache)
def get_mapper_id_str(cursor, key_value, key_type):
    """
    获取id
    :param cursor: DictCursor
    :param key_value:
    :param key_type:
    :return:
    """
    sql = 'select id from `IdMapper` where `key` = %s and `type` = %s'
    count = cursor.execute(sql, (key_value, key_type))

    if count == 0:
        sql = "insert into `IdMapper` (`key`, `type`, `created_time`) values (%s, %s, %s)"
        cursor.execute(sql, (key_value, key_type, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        mapper_id = int(cursor.lastrowid)
    else:
        item = cursor.fetchone()
        mapper_id = item['id']

    return mapper_id


def generate_attachment_path_name(flag, save_time):
    # 按照年月分目录
    if flag:
        path = '/'.join([base_att_path, flag, save_time[:7], ''])
    else:
        path = '/'.join([base_att_path, save_time[:7], ''])
    name = save_time + '.txt'
    return path, name


def save_attachment(flag, save_time):
    """
    保存文件附件
    :param flag: 附件区别, str, 'mysql'
    :param save_time: 文件保存时间, str, '2017-01-01 00:00:00'
    :return: path, name
    """
    path_file = '/dev/null'
    path, name = generate_attachment_path_name(flag, save_time)

    if not os.path.exists(path):
        os.makedirs(path)

    if transfer_log_deque:
        path_file = path + name
        with open(path+name, 'a') as fp:
            fp.write('\n'.join(transfer_log_deque))
    return path_file


def send_notification_mail(content, subject=u'Notification', att_path=None):
    """
    发送报警邮件
    :param subject: 邮件主题, str
    :param content: 邮件内容, str
    :param att_path: 邮件附件列表，list
    :return:
    """
    from_add = 'data.admin@sfy.com'
    to_addrs = ['zheng.long@sfy.com']
    password = '1A2b3cAdmin'

    send_mail(subject, content, to_addrs, from_add, password, att_path)


def create_transfer_log(des_cr, from_table, to_table, from_rows, to_rows, count_time):
    """
    数据同步完成后记录同步结果
    :param des_cr: 目标数据库 cursor, type: SSDictCursor or DictCursor
    :param from_table: 源数据库表
    :param to_table: 目标数据库表
    :param from_rows: 读取数量
    :param to_rows: 写入数量
    :param count_time: 分割时间
    :return:
    """
    logger.info(from_table + ': ' + str(from_rows) + ' ' + to_table + ': ' + str(to_rows))

    if from_rows <= 0:
        return

    record_sql = """INSERT INTO sfy_bi.TransferLog 
                    (from_table, to_table, from_count, to_count, count_time) VALUES (%s, %s, %s, %s, %s);"""
    des_cr.execute(record_sql, (from_table, to_table, from_rows, to_rows, count_time))

    # 迁移前后数量不一致
    if from_rows > (to_rows+5):
        logger.info('from ' + from_table + ' to ' + to_table + ' sync count not equal')
        content = u'在同步 ' + from_table + u' 到 ' + to_table + u' 时，同步数据不一致，请查看日志！'
        transfer_log_deque.append(content)
