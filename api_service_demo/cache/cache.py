#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
from pymysql.cursors import DictCursor

from common.dbhelper import DBHelper
from settings import system_config
from cache.base import Cache

REDIS_CONFIG = system_config.get('REDIS_CONFIG')
sfy_RISK_CONFIG = system_config.get('sfy_RISK_CONFIG')


class HangjuXfnlParamCache(object):
    def __init__(self):
        self.cache = Cache('HangjuXfnlParam', **REDIS_CONFIG)

    def get(self, key):
        return self.cache.get(key)

    def init(self):
        """
        初始化缓存，
        :return:
        """
        db = DBHelper(DictCursor, **sfy_RISK_CONFIG)
        cursor = db.cr

        sql = """SELECT score, frequency_lower, frequency_upper, discount_rate_lower, 
            discount_rate_upper, amount_lower, amount_upper FROM sfy_risk.HangjuXfnlParam"""
        cursor.execute(sql)
        values = cursor.fetchall() or []

        ret = {val['score']: val for val in values}
        self.cache.setm(ret)

        db.close()


class LocationCache(object):
    def __init__(self):
        self.cache = Cache('Location', **REDIS_CONFIG)

    def get(self, key):
        return self.cache.get(key)

    def init(self):
        """
        初始化缓存，
        :return:
        """
        db = DBHelper(DictCursor, **sfy_RISK_CONFIG)
        cursor = db.cr

        limit = 3000
        offset = 0

        while 1:
            sql = """SELECT code, province, city, corporation, area_code, zip_code
                FROM sfy_risk.PhoneCity limit %s offset %s"""
            result = cursor.execute(sql, (limit, offset))
            values = cursor.fetchall() or []

            ret = {val['code']: val for val in values}
            self.cache.setm(ret)

            offset += result
            if result < limit:
                break

        db.close()


if __name__ == '__main__':
    pass
