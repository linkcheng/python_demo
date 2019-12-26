#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import time
import sys
import re
import logging
import getopt
from datetime import datetime, date, timedelta
from functools import wraps

logger = logging.getLogger(__name__)

__all__ = [
    'IS_DEBUG',
    'is_valid_phone',
    'fn_timer',
    'format_value',
    'fmt_replace_sql',
]

IS_DEBUG = False

str_fmt = '%Y-%m-%d %H:%M:%S'


def fmt_replace_sql(table, columns):
    """
    格式化 replace sql
    :param table: 表名  'table1'
    :param columns: 列 [col1, col2]
    :return:
    """
    return 'REPLACE INTO sfy_bi.{0} ({1}) VALUES ({2})'.\
        format(table, ','.join(['`' + col + '`' for col in columns]), ','.join(['%s']*len(columns)))


class TimeSeries(object):

    def __init__(self, start_time, end_time, days=0, hours=4):
        self.current = start_time
        self.end_time = end_time
        self.days = days
        self.hours = hours
        self.__is_stop = False

    def __iter__(self):
        return self

    def __next__(self):
        return self.next()

    def next(self):
        if self.__is_stop:
            raise StopIteration

        current = self.current

        self.current += timedelta(days=self.days, hours=self.hours)
        if self.current >= self.end_time:
            self.__is_stop = True

        return current


def build_time_str_list(start_str, end_str, days=0, hours=4):
    """
    生产从 start_str 到 end_str，步长为 days and hours 的时间字符串列表
    :param start_str:
    :param end_str:
    :param days:
    :param hours:
    :return:
        start_str > end_str -> []
        start_str = end_str -> [end_str]
        start_str < end_str -> [start_str, ..., end_str]
    """
    if start_str > end_str:
        return []

    start_time = datetime.strptime(start_str, str_fmt)

    time_str_list = [start_str]

    while start_str < end_str:
        start_time += timedelta(days=days, hours=hours)
        start_str = start_time.strftime(str_fmt)
        time_str_list.append(start_str)

    time_str_list[-1] = end_str

    return time_str_list


def format_value(value):
    if value is None:
        value = 'null'

    elif isinstance(value, (basestring, datetime, date)):
        value = re.sub("'", "", str(value))
        value = "'" + str(value) + "'"

    return value


formatValue = format_value


def is_valid_phone(number):
    """
    判断是否是手机号
    :return:
    """

    num = re.match(r'1[3-9]\d{9}', number)
    return True if num else False


def fn_timer(fn):
    """
    计算 fn 的运算时间
    :param fn:
    :return:
    """
    @wraps(fn)
    def function_timer(*args, **kwargs):
        start = time.time()
        result = fn(*args, **kwargs)
        end = time.time()
        logger.info('Total running time %s seconds' % str(end - start))
        return result

    return function_timer


def cmd():
    """
    获取命令行参数
    :return:
    """
    opts, args = getopt.getopt(sys.argv[1:], 'd')
    global IS_DEBUG

    for opt, value in opts:
        IS_DEBUG = True if '-d' == opt else False


cmd()
