#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author: Link 
@contact: zheng.long@sfy.com
@module: kafka.py
@date: 2019-05-20 
"""

from pykafka import KafkaClient

hosts = "192.168.30.141:6667,192.168.30.140:6667,192.168.30.139:6667"
TOPIC = 'test_kafka_topic'


def producer():
    client = KafkaClient(hosts=hosts)
    # 查看所有的topic
    # client.topics
    print(client.topics)

    # 选择一个topic
    topic = client.topics[TOPIC]
    message = "test message test message"

    # 当有了topic之后呢，可以创建一个producer,来发消息，生产kafka数据,通过字符串形式，
    with topic.get_sync_producer() as producer:
        producer.produce(message)

    with topic.get_sync_producer() as producer:
        producer.produce('test message', partition_key='1')

    # 但生产环境，为了达到高吞吐量，要采用异步的方式，通过 delivery_reports = True 来启用队列接口
    producer = topic.get_producer(delivery_reports=True)
    producer.produce(message)
    producer.stop()

    print(message)


def produce_users():
    from datetime import datetime
    import time
    import json
    hosts = "192.168.30.141:6667,192.168.30.140:6667,192.168.30.139:6667"
    topic = "v2.User1"

    client = KafkaClient(hosts=hosts)
    # 选择一个topic
    topic = client.topics[topic]

    with topic.get_sync_producer() as prod:
        for i in range(1000):
            user = {
                'mobile': 'mobile' + str(i),
                'name': 'name' + str(i),
                'created_time': datetime.now().strftime('%Y-%pattern-%d %H:%M:%S')
            }
            prod.produce(json.dumps(user))
            time.sleep(10)


def consumer():
    client = KafkaClient(hosts=hosts)
    topic = client.topics[TOPIC]

    # 从zookeeper消费，zookeeper的默认端口为2181
    balanced_consumer = topic.get_balanced_consumer(
        consumer_group='test_kafka_group',
        # 设置为False的时候不需要添加consumer_group，直接连接topic即可取到消息
        auto_commit_enable=True,
        zookeeper_connect='hh001:2181,hh002:2181,hh0013:2181'
    )

    partitions = topic.partitions
    print("分区 {}".format(partitions))
    earliest_offsets = topic.earliest_available_offsets()
    print("最早可用offset {}".format(earliest_offsets))
    last_offsets = topic.latest_available_offsets()
    print("最近可用offset {}".format(last_offsets))
    offset = balanced_consumer.held_offsets
    print("当前消费者分区offset情况{}".format(offset))

    """
    LAST_N_MESSAGES = 50
    # how many messages should we get from the end of each partition?
    MAX_PARTITION_REWIND = int(math.ceil(LAST_N_MESSAGES / len(consumer._partitions)))
    # find the beginning of the range we care about for each partition
    offsets = [(string, op.last_offset_consumed - MAX_PARTITION_REWIND)
               for string, op in balanced_consumer._consumer._partitions.items()]
    # if we want to rewind before the beginning of the partition, limit to beginning
    offsets = [(string, (o if o > -1 else -2)) for string, o in offsets] 
    # reset the consumer's offsets
    balanced_consumer.reset_offsets(offsets)
    balanced_consumer.reset_offsets([(topic.partitions[0], -2), (topic.partitions[1], 10)])

    """
    balanced_consumer.reset_offsets([()])

    for message in balanced_consumer:
        # print message
        if message is not None:
            # 打印接收到的消息体的偏移个数和值
            print(message.partition, message.offset, message.value)
