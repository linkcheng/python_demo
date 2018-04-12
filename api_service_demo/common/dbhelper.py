#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
import pymysql
from DBUtils.PooledDB import PooledDB


class BaseDBHelper(object):
    def __init__(self, db_type, cursor_type, **kwargs):
        self.pool = PooledDB(db_type, **kwargs)
        self.conn = self.pool.connection()
        self.cr = self.conn.cursor(cursor_type)

    def __del__(self):
        self.close()

    def commit(self):
        self.conn.commit()

    def close(self):
        self.cr.close()
        self.conn.close()
        self.pool.close()


class MysqlDBHelper(BaseDBHelper):
    def __init__(self, cursor_type, **kwargs):
        super(MysqlDBHelper, self).__init__(pymysql, cursor_type, **kwargs)


DBHelper = MysqlDBHelper
