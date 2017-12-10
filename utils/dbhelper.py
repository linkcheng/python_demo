#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import pymysql
import phoenixdb

__all__ = [
    'DBHelper', 'MysqlDBHelper', 'PhoenixDBHelper'
]


class DBHelperMixin(object):
    def commit(self):
        self.conn.commit()

    def close(self):
        self.commit()
        self.cr.close()
        self.conn.close()


class BaseDBHelper(DBHelperMixin):
    def __init__(self, db_type, cursor_type, **kwargs):
        self.conn = db_type.connect(**kwargs)
        self.cr = self.conn.cursor(cursor_type)


class MysqlDBHelper(BaseDBHelper):
    def __init__(self, cursor_type, **kwargs):
        super(MysqlDBHelper, self).__init__(pymysql, cursor_type, **kwargs)


class PhoenixDBHelper(BaseDBHelper):
    def __init__(self, cursor_type, **kwargs):
        super(PhoenixDBHelper, self).__init__(phoenixdb, cursor_type, **kwargs)


DBHelper = MysqlDBHelper
