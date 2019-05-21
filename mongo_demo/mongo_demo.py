#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author: Link 
@contact: zheng.long@shoufuyou.com
@module: mongo_demo 
@date: 2019-05-14 
"""
from pymongo import MongoClient

IP = '127.0.0.1'
MONGO_URI = (
    'mongodb://admin:x&1dyERcrBgh#!Cd'
    f'@{IP}:27017/?authSource=admin&authMechanism=SCRAM-SHA-1'
)
DB_NAME = 'reporting'
COLLECTION_NAME = 'bizEventReport2019'


def query(db=DB_NAME, col=COLLECTION_NAME):
    client = MongoClient(MONGO_URI)
    db = client[db]
    col = db[col]

    domain = {'created_time': {'$gte': '2019-05-14'}}
    fields = {
        '_id': 0,
        'event_id': 1,
        'app_name': 1,
        'mobile': 1,
        'created_time': 1,
    }
    values = col.find(domain, fields)

    for val in values:
        print(val)


def watch(db=DB_NAME, col=COLLECTION_NAME):
    client = MongoClient(MONGO_URI)
    db = client[db]
    col = db[col]

    with col.watch() as stream:
        for change in stream:
            print(change)


if __name__ == '__main__':
    watch()
