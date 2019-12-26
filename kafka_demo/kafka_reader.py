#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author: Link 
@contact: zheng.long@sfy.com
@module: kafka_reader 
@date: 2019-06-03 
"""
import logging

from pykafka.common import OffsetType

from readers.mq_base import MQReader
from connectors.kafka_connector import KafkaConnector

from config.sys_config import USE_RDKAFKA_C, BOOTSTRAP_SERVERS

logger = logging.getLogger(__name__)


class PyKafkaReader(MQReader):
    @staticmethod
    def decode(args):
        k, v = args
        return int(k), int(v)

    @staticmethod
    def get_value(msg):
        return msg.value

    @staticmethod
    def get_token(msg):
        # todo: not sure whether needs + 1
        return {msg.partition_id: msg.offset}

    def __init__(self, topic_name, group_id='group-1',
                 bootstrap_servers=BOOTSTRAP_SERVERS,
                 is_bootstrap=True, is_resume=True):
        """从 Kafka 读取数据
        :param topic_name: str, kafka topic
        :param group_id: str, kafka topic group_id
        :param bootstrap_servers: kafka host
        :param is_bootstrap: 是否全量读取
        :param is_resume: 是否断点续传
        """
        self.group_id = group_id
        super().__init__(f'kafka:{topic_name}:{self.group_id}',
                         is_bootstrap=is_bootstrap, is_resume=is_resume)

        self.conn = KafkaConnector(bootstrap_servers, topic_name)
        self.client = self.conn.client
        self.topic = self.client.topics[topic_name]
        self.consumer = self.topic.get_balanced_consumer(
                consumer_group=self.group_id,
                auto_commit_enable=True,
                auto_offset_reset=OffsetType.EARLIEST if is_bootstrap else OffsetType.LATEST,
                zookeeper_connect=self.conn.zk_hosts,
                use_rdkafka=USE_RDKAFKA_C,
            )

    def read(self):
        """
        partitions = self.topic.partitions
        print(f"分区 {partitions}")
        earliest_offsets = self.topic.earliest_available_offsets()
        print(f"最早可用offset {earliest_offsets}")
        last_offsets = self.topic.latest_available_offsets()
        print(f"最近可用offset {last_offsets}")
        offset = self.consumer.held_offsets
        print(f"当前消费者分区offset情况{offset}")
        """
        partitions: dict = self.topic.partitions

        if self.is_resume and self.resume_token:
            partition_offsets = [
                (partitions[p_id], (o if o > OffsetType.LATEST else OffsetType.EARLIEST))
                for p_id, o in self.resume_token.items()
            ]
            self.consumer.reset_offsets(partition_offsets)

        for msg in self.consumer:
            logger.info(f'{self.topic} {msg.partition_id} {msg.offset}')
            yield msg

    def stop(self):
        try:
            self.consumer.stop()
        except RuntimeError:
            pass
        super().stop()
        logger.info(f'Kafka reader [{self.conn.topic_name}] stopped')


if __name__ == '__main__':
    import json

    from config.sys_config import BOOTSTRAP_SERVERS as KFK_HOSTS

    from utils.log import configure_logging

    configure_logging()
    logger = logging.getLogger(__name__)

    kr = PyKafkaReader(KFK_HOSTS, 'reporting-bizEventReport2019', True, True)
    try:
        for m in kr.read():
            print(m.partition_id, m.offset, json.loads(m.value))
    finally:
        kr.stop()
