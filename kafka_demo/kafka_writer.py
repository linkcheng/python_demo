#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author: Link 
@contact: zheng.long@sfy.com
@module: kafka_writer 
@date: 2019-06-13 
"""
import logging
from pykafka.common import CompressionType

from connectors.kafka_connector import KafkaConnector
from writers.base import BaseWriter
from utils.common import obj2bytes
from config.sys_config import USE_RDKAFKA_P, MESSAGE_MAX_BYTES
from config.sys_config import BOOTSTRAP_SERVERS

logger = logging.getLogger(__name__)


class PyKafkaWriter(BaseWriter):
    def __init__(self, topic_name, bootstrap_servers=BOOTSTRAP_SERVERS,
                 *args, **kwargs):
        self.conn = KafkaConnector(bootstrap_servers, topic_name)
        self.client = self.conn.client
        self.topic = self.client.topics[topic_name]
        self.producer = self.topic.get_producer(
            compression=CompressionType.SNAPPY,
            use_rdkafka=USE_RDKAFKA_P,
            max_request_size=MESSAGE_MAX_BYTES,
        )

    def write(self, obj):
        """写入 kafka
        获取 delivery_report
        Returns 2-tuples of a `pykafka.protocol.Message` and either `None`
        (for successful deliveries) or `Exception` (for failed deliveries).
        """
        self.producer.produce(obj2bytes(obj))

        # message, ret = self.producer.get_delivery_report()
        # if ret is not None:
        #     raise ret

    def commit(self, *args, **kwargs):
        pass

    def stop(self):
        super().stop()
        self.producer.stop()
        logger.info(f'Kafka writer [{self.conn.topic_name}] stopped')


if __name__ == '__main__':
    import json

    from config.sys_config import BOOTSTRAP_SERVERS as KFK_HOSTS

    ms = [
        {
            '_id': {
                '_data': '825D01F8F20000000129295A1004CA2EF16C952B4DFDA0B8A911DD5E4CD946645F696400645D01F8EEC665DA3DC9D421850004'
            },
            'operationType': 'insert',
            'clusterTime': (1560410354, 1),
            'fullDocument': {
                '_id': ('5d01f8eec665da3dc9d42185'),
                'lm_number': '2018122614102739934561',
                'app_name': 'xyf',
                'event_id': '1002107',
                'device_id': '20190613f538e1088',
                'user_id': '6065750',
                'session_id': '3783747965704725f0d42633a247f180',
                'source_type': 'client',
                'position': '2',
                'event_time': '1560410269041',
                'is_login': '1',
                'mobile': '13186668169',
                'token': '3783747965704725f0d42633a247f180',
                'os': 'android',
                'app': 'xyf',
                'channel': 'autoupdate',
                'version_code': '30400',
                'utm_source': '',
                'created_time': '2019-06-13 15:17:54'
            },
            'ns': {
                'db': 'reporting',
                'coll': 'bizEventReport2019'
            },
            'documentKey': {
                '_id': ('5d01f8eec665da3dc9d42185')
            }
        },
        {
            '_id': {
                '_data': '825D01FA7B0000000129295A1004CA2EF16C952B4DFDA0B8A911DD5E4CD946645F696400645D01FA7745C4B16BB4CFB1C50004'
            },
            'operationType': 'insert',
            'clusterTime': (1560410747, 1),
            'fullDocument': {
                '_id': ('5d01fa7745c4b16bb4cfb1c5'),
                'event_id': '1002466',
                'mobile': '',
                'type': '8',
                'event_time': '1560410274784',
                'token': 'eab967b7a66cb969333163a1ae183bad',
                'device_id': '',
                'source_type': 'wap',
                'os': 'ios',
                'app': 'xyf',
                'channel': '',
                'version_code': '',
                'utm_source': 'QD-CPS-XYF-YJ01',
                'created_time': '2019-06-13 15:17:54'
            },
            'ns': {
                'db': 'reporting',
                'coll': 'bizEventReport2019'
            },
            'documentKey': {
                '_id': ('5d01fa7745c4b16bb4cfb1c5')
            }
        }
    ]

    kw = PyKafkaWriter('reporting-bizEventReport2019-1')
    kw.producer.start()
    for m in ms:
        print(m)
        kw.write(bytes(json.dumps(m), encoding='utf-8'))
    # kw.commit()
    kw.stop()
