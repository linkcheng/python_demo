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
    is_active = BooleanField('激活状态', default=True)


class User(Base):
    """
        create table server_user (
            id int unsigned not null auto_increment comment '主键自增id'
            ,username varchar(32) not null default '' comment '用户名'
            ,password varchar(256) not null default '' comment '密码'
            ,mobile varchar(12) not null default '' comment '手机号'
            ,email varchar(128) not null default '' comment '邮箱'
            ,created_time timestamp not null default CURRENT_TIMESTAMP COMMENT '创建时间'
            ,updated_time timestamp not null default CURRENT_TIMESTAMP on update CURRENT_TIMESTAMP COMMENT '更新时间'
            ,is_active tinyint(1) NOT NULL DEFAULT 1 COMMENT '是否有效'
            ,primary key(id)
            ,unique key uniq_username(username)
            ,unique key uniq_mobile(mobile)
        ) engine=innodb default charset=utf8 comment '用户表'
        ;
    """
    class Meta:
        db_table = 'server_user'

    username = CharField('用户名', max_length=32, null=False, default='')
    password = CharField('密码', max_length=256, null=False, default='')
    mobile = CharField('手机号', max_length=12, null=False, default='')
    email = EmailField('邮箱地址', max_length=128, null=False, default='')

    def __str__(self):
        return self.username

    @classmethod
    def get_user(cls, username, password):
        try:
            user = cls.objects.get(username=username, password=password)
        except cls.DoesNotExist:
            user = None
        return user

