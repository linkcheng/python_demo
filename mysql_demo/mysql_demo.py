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
                print(message.offset, message.value)
    except KeyboardInterrupt:
        print(message.offset if message else 0)


class SQLBuilder:
    route_table = {
        'insert': ('insert', 'bootstrap-insert'),
        'update': ('update', ),
        'delete': ('delete', ),
        'table-alter': ('alter table', ),
    }

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
        self.columns = columns
        self.mode = mode
        self.sql_template = self.insert_sql_template(mode)
        self.sql = None
        if columns:
            self.sql = self.sql_format(
                self.sql_template,
                self.database,
                self.table,
                self.columns
            )

    @staticmethod
    def sql_format(sql, database, table, columns):
        return sql.format(database=database, table=table, columns=columns, )

    @staticmethod
    def insert_sql_template(mode):
        if not mode:
            sql = """
                insert into `{database}`.`{table}` ({','.join(columns)}) 
                values ({','.join(['%s'] * len(columns))});
            """
        elif mode == 'ignore':
            sql = """
                insert ignore into `{database}`.`{table}` ({','.join(columns)}) 
                values ({','.join(['%s'] * len(columns))});
            """
        elif mode == 'replace':
            sql = """replace into `{database}`.`{table}` ({','.join(columns)}) 
                values ({','.join(['%s'] * len(columns))});"""
        else:
            sql = ""
        return sql

    @staticmethod
    def insert_values(datas, keys):
        return [[data.get(k) for k in keys] for data in datas]

    def route(self, values):
        router = {
            'insert': [],
            'update': [],
            'delete': [],
        }
        for value in values:
            action_type = value.get('type')
            if action_type in self.route_table['insert']:
                router['insert'].append(value)
            elif action_type in self.route_table['update']:
                router['update'].append(value)
            elif action_type in self.route_table['delete']:
                router['delete'].append(value)

    def insert(self, value, keys=None):
        """\
        基于原始数据生成 insert_ignore_sql
        :param value: 数据
        {
            "database": "test",
            "table": "User",
            "type": "bootstrap-insert",
            "ts": 1558339701,
            "data": {
                "id": 1,
                "name": null,
                "mobile": "15888888888",
                "password_digest": "",
                "email": null,
                "created_time": "2019-05-18 17:59:59",
                "last_login_time": "2019-05-18 17:59:59",
                "gender": "other",
                "person_id": 0,
                "utm_source": "小白信用分",
                "updated_time": "2019-05-18 17:59:59",
            }
        }
        :param keys: None or [],
            表示从 value 中获取的数据关键字，
            如果为 None 表示使用 value 中 data 的所有 key
        :return: SQL: str
        """
        data = value.get('data')

        if not data:
            # 没有数据表示没有数据，不能生成 sql
            return ''

        if not keys:
            keys = list(data.keys())

        vals = self.insert_values(data, keys)

        sql = self.sql_format(
            self.sql_template,
            self.database,
            self.table,
            self.columns
        )


if __name__ == '__main__':
    read_from_kafka(HOSTS, 'ns_alluser_xinyongfei_cs_StarUser')
