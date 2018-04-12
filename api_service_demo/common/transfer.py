#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


def s2d(val, fmt):
    """字符串转date"""
    ret = s2t(val, fmt)
    return ret.date() if ret else None


def s2t(val, fmt):
    """字符串转datetime"""
    try:
        ret = datetime.strptime(val, fmt) if val else None
    except Exception as e:
        logger.info(str(e))
        ret = None
    return ret


def s2i(val, default=None):
    """字符串转整数"""
    if isinstance(val, str) and ':' in val:
        return default

    try:
        ret = int(val) if val is not None else default
    except Exception as e:
        logger.info(str(e))
        ret = default
    return ret


def s2f(val):
    """字符串转小数"""
    try:
        ret = float(val) if val else None
    except Exception as e:
        logger.info(str(e))
        ret = None
    return ret


def s2num(val):
    """低效将字符串转数字，但兼容性好"""
    if val in (u'否', ):
        val = '0'
    elif val in (u'是', ):
        val = '1'

    try:
        ret = eval(val) if val else None
    except Exception as e:
        logger.info(str(e))
        ret = None

    # 非数字类型的值
    if not isinstance(ret, (int, float, )):
        ret = None
    return ret


def b2s(val):
    """byte -> str"""
    if isinstance(val, bytes):
        val = val.decode('utf-8')

    return val


def s2b(val):
    """str -> byte"""
    if isinstance(val, str):
        val = val.encode('utf-8')

    return val


def ensure_unicode(val):
    return b2s(val)


if __name__ == '__main__':
    print(s2num('是'))
    print(s2num('否'))
    print(s2f('1.2'))
    print(s2i(1))
    print(s2i('2'))
    print(s2t('2018-01-01 10:00:00', '%Y-%m-%d %H:%M:%S'))
    print(s2d('2018-01-01 10:00:00', '%Y-%m-%d %H:%M:%S'))
    print(s2d('2018-01-01 10-00-00', '%Y-%m-%d %H:%M:%S'))
