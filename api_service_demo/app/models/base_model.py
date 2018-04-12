#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
from datetime import datetime
from peewee import *
from register import db


class BaseModel(Model):
    """ 基础类
    https://github.com/coleifer/peewee/blob/master/docs/peewee/database.rst
    """
    class Meta:
        database = db
        # order by created date descending
        ordering = (('created_time', 'desc'), )

    created_time = DateTimeField(default=datetime.now)
    updated_time = DateTimeField(default=datetime.now)

    @classmethod
    def update(cls, __data=None, **update):
        update.update(updated_time=datetime.now())
        return super(BaseModel, cls).update(__data, **update)

    @classmethod
    def get_one(cls, *query, **kwargs):
        """查询不到返回None，而不抛出异常"""
        try:
            return cls.get(*query, **kwargs)
        except DoesNotExist:
            return None
