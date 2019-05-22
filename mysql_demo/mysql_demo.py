#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author: Link 
@contact: zheng.long@shoufuyou.com
@module: mysql_demo 
@date: 2019-05-20
@note:
    ImportError: Please install python-snappy
    pip install python-snappy
"""
from werkzeug.utils import cached_property
from pykafka import KafkaClient
from pykafka.common import OffsetType

HOSTS = "hh001:6667,hh002:6667,hh003:6667"
ZK_HOSTS = 'hh001:2181,hh002:2181,hh003:2181'

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


def read_from_kafka(hosts: str, topic_name: str, zk_hosts: str = ZK_HOSTS):
    client = KafkaClient(hosts=hosts)
    topic = client.topics[topic_name]
    message = None

    # 从zookeeper消费，zookeeper的默认端口为2181
    balanced_consumer = topic.get_balanced_consumer(
        consumer_group=f'{topic_name}_group',
        # 设置为False的时候不需要添加consumer_group，直接连接topic即可取到消息
        auto_commit_enable=True,
        zookeeper_connect=zk_hosts
    )

    try:
        for message in balanced_consumer:
            # print message
            if message is not None:
                # 打印接收到的消息体的偏移个数和值
                yield (message.offset, message.value)
    except KeyboardInterrupt:
        print(message.offset if message else 0)


class SQLBuilder:
    def __init__(self, database, table, columns=None, mode=None):
        """\
        构造器
        :param columns: [] or None, 数据表的列
            如果为 None，表示从原数据提取
        :param mode: 在 insert 时，有几种种模式可选
            None: 原生模式
            ignore: 新数据重复忽略，依赖 unique key
            replace：新数据重复替换，生成新 id
        """
        self.database = database
        self.table = table
        self.mode = mode
        self.columns = None
        if columns:
            self.build(columns)

    @property
    def sql(self):
        """\
        暂且仅 insert 模式支持
        :return:
        """
        if not self.mode:
            sql = f"""insert into `{self.database}`.`{self.table}` ({','.join(self.columns)}) 
                values ({','.join(['%s'] * len(self.columns))});"""
        elif self.mode == 'ignore':
            sql = f"""insert ignore into `{self.database}`.`{self.table}` ({','.join(self.columns)}) 
                values ({','.join(['%s'] * len(self.columns))});"""
        elif self.mode == 'replace':
            sql = f"""replace into `{self.database}`.`{self.table}` ({','.join(self.columns)}) 
                values ({','.join(['%s'] * len(self.columns))});"""
        else:
            sql = ""
        return sql

    def build(self, columns):
        self.columns = columns
        return self.sql

    def insert(self, datas, keys=None, columns=None):
        """\
        基于原始数据生成 insert_ignore_sql
        :param datas: 数据
        [
            {
                "id": 1,
                "mobile": "15888888888",
                "created_time": "2019-05-18 17:59:59",
                "gender": "other",
                "utm_source": "小白信用分",
                "updated_time": "2019-05-18 17:59:59",
            },
            {}
        ]
        :param keys: None or [],
            表示从 value 中获取的数据关键字，
            如果为 None 表示使用 value 中 data 的所有 key
        :param columns: None or [], 数据表的列
            如果为 None，表示从原数据提取
        :return: SQL: str
        """
        if len(datas) > 0:
            data = datas[0]
        else:
            return

        if not keys:
            keys = list(data.keys())

        if not columns:
            columns = self.columns or keys

        sql = self.sql if columns == self.columns else self.build(columns)
        values = [[data.get(k) for k in keys] for data in datas if data]

        return sql, values


class BootstrapInsert:
    route_table = {
        'insert': ('insert', 'bootstrap-insert'),
        'update': ('update', ),
        'delete': ('delete', ),
        'table-alter': ('alter table', ),
    }

    def __init__(self, values):
        self.insert = []
        self.update = []
        self.delete = []

        for value in values:
            action_type = value.get('type')
            if action_type in self.route_table['insert']:
                self.insert.append(value)
            elif action_type in self.route_table['update']:
                self.update.append(value)
            elif action_type in self.route_table['delete']:
                self.delete.append(value)


if __name__ == '__main__':
    # offset, value = read_from_kafka(HOSTS, 'ns_alluser_xinyongfei_cs_StarUser')

    db, t = 'xinyongfei_cs', 'StarUser'
    datas = [
        {
            "id": 1,
            "mobile": "15888888888",
            "created_time": "2019-05-18 17:59:59",
            "gender": "other",
            "utm_source": "小白信用分",
            "updated_time": "2019-05-18 17:59:59",
        },
    ]
    builder = SQLBuilder(db, t)
    print(builder.insert(datas))
