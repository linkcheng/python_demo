#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author: Link 
@contact: zheng.long@sfy.com
@module: kafka_connector 
@date: 2019-06-16 
"""
import logging
from pykafka import KafkaClient

from config.sys_config import ZK_HOSTS, BROKER_VERSION

logger = logging.getLogger(__name__)


class KafkaConnector:
    def __init__(self, hosts: str, topic_name: str, zk_hosts: str = ZK_HOSTS):
        self.hosts = hosts
        self.topic_name = topic_name
        self.zk_hosts = zk_hosts
        self.client = KafkaClient(hosts=hosts, broker_version=BROKER_VERSION)
        self.topic = self.client.topics[topic_name]


if __name__ == '__main__':
    pass
