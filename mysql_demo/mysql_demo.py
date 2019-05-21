#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author: Link 
@contact: zheng.long@shoufuyou.com
@module: mysql_demo 
@date: 2019-05-20 
"""
from pykafka import KafkaClient

hosts = "192.168.30.141:6667,192.168.30.140:6667,192.168.30.139:6667"
TOPIC = 'test_kafka_topic'

IP = '127.0.0.1'
DB = 'shoufuyou_v2'

DB_CONFIG = {
    'host': IP,
    'port': 3306,
    'user': 'root',
    'password': 'xzQPRzgoLKwMpt*#A#ir',
    'db': DB,
    'charset': 'utf8',
}


def read_from_kafka():
    client = KafkaClient(hosts=hosts)
    topic = client.topics[TOPIC]

    # 从zookeeper消费，zookeeper的默认端口为2181
    balanced_consumer = topic.get_balanced_consumer(
        consumer_group='test_kafka_group',
        # 设置为False的时候不需要添加consumer_group，直接连接topic即可取到消息
        auto_commit_enable=True,
        zookeeper_connect='hh001:2181,hh002:2181,hh0013:2181'
    )

    for message in balanced_consumer:
        # print message
        if message is not None:
            # 打印接收到的消息体的偏移个数和值
            print(message.offset, message.value)


def insert_into_db():
    pass


if __name__ == '__main__':
    pass
