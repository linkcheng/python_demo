#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
from django.db import models
from django.db.models.fields import *
from django.db.models.fields.related import *
import django.utils.timezone as timezone


class Base(models.Model):
    id = AutoField('主键', primary_key=True)
    created_time = DateTimeField('创建时间', default=timezone.now)
    updated_time = DateTimeField('更新时间', auto_now=True)
    is_active = BooleanField('激活状态', default=True)

    class Meta:
        abstract = True


class Menu(Base):
    """
    菜单表
    """
    title = models.CharField(verbose_name='菜单名称', max_length=32)
    icon = models.CharField(verbose_name='图标', max_length=32)

    def __str__(self):
        return self.title


class Permission(models.Model):
    """
    权限表
    """
    title = models.CharField(verbose_name='标题', max_length=32)
    url = models.CharField(verbose_name='含正则的URL', max_length=128)
    name = models.CharField(verbose_name='URL别名', max_length=32, unique=True)
    menu = models.ForeignKey(verbose_name='所属菜单', to='Menu', null=True, blank=True, help_text='null表示不是菜单;非null表示是二级菜单')
    pid = models.ForeignKey(verbose_name='关联的权限', to='Permission', null=True, blank=True, related_name='parents',
                            help_text='对于非菜单权限需要选择一个可以成为菜单的权限，用户做默认展开和选中菜单')

    def __str__(self):
        return self.title


class Role(models.Model):
    """
    角色
    """
    title = models.CharField(verbose_name='角色名称', max_length=32)
    permissions = models.ManyToManyField(verbose_name='拥有的所有权限', to='Permission', blank=True)

    def __str__(self):
        return self.title


class UserInfo(Base):
    """
    用户表
    """
    name = CharField('用户名', max_length=32, null=False, default='')
    password = CharField('密码', max_length=255, null=False, default='')
    mobile = CharField('手机号', max_length=12, unique=True, null=False, default='')
    email = EmailField('邮箱', max_length=128, null=False, default='')
    roles = ManyToManyField('拥有的所有角色', to=Role, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'user_info'
        ordering = ['created_time']
        verbose_name = '用户'
