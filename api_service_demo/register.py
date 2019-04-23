#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
from pymongo import MongoClient
from pymysql.cursors import DictCursor
from peewee import MySQLDatabase
from settings import system_config
from common.dbhelper import DBHelper


db = MySQLDatabase(MODEL, **MODEL_CONFIG)


