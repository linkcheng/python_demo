#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
from django.db import models
from django.db.models.fields import *
import django.utils.timezone as timezone


class Base(models.Model):
    class Meta:
        abstract = True

    id = AutoField('主键', primary_key=True)
    created_time = DateTimeField('创建时间', default=timezone.now)
    updated_time = DateTimeField('更新时间', auto_now=True)
    is_active = BooleanField('激活状态', default=False)


class User(Base):
    name = CharField('用户名', max_length=32, null=False, default='')
    password = CharField('密码', max_length=256, null=False, default='')
    mobile = CharField('手机号', max_length=12, null=False, default='')
    email = EmailField('邮箱地址', max_length=128, null=False, default='')

    def __str__(self):
        return self.name


