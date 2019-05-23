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
import time
import signal
from abc import ABCMeta, abstractmethod
from queue import Queue, Empty
from threading import Thread

import pymysql
from pymysql.cursors import DictCursor
from pymysql.err import Error, OperationalError
from pykafka import KafkaClient

HOSTS = "hh001:6667,hh002:6667,hh003:6667"
ZK_HOSTS = 'hh001:2181,hh002:2181,hh003:2181'

IP = '127.0.0.1'
# DB = 'shoufuyou_v2'
DB = 'shoufuyou_statistics'

DB_DEFAULT_CONFIG = {
    'host': IP,
    'port': 3306,
    'user': 'root',
    'password': '12345678',
    # 'password': 'xzQPRzgoLKwMpt*#A#ir',
    'db': DB,
    'charset': 'utf8',
}

CONFIG = {
    'shoufuyou_v2': DB_DEFAULT_CONFIG,
    'shoufuyou_statistics': DB_DEFAULT_CONFIG,
    'xinyongfei_cs': DB_DEFAULT_CONFIG,
}


class MySQLDBHelper:
    def __init__(self, **kwargs):
        self.conn = pymysql.connect(**kwargs)
        self.cr = self.conn.cursor(DictCursor)

    def __del__(self):
        self.close()

    def execute(self, sql, args=None):
        try:
            result = self.cr.execute(sql, args)
        except OperationalError:
            self.conn.ping()
            result = self.cr.execute(sql, args)
        return result

    def executemany(self, sql, args=None):
        try:
            result = self.cr.executemany(sql, args)
        except OperationalError:
            self.conn.ping()
            result = self.cr.execute(sql, args)
        return result

    def rollback(self):
        self.conn.rollback()

    def commit(self):
        self.conn.commit()

    def close(self):
        self.cr.close()
        try:
            self.conn.close()
        except Error:
            pass


class Reader:
    def __init__(self):
        self.observers = []

    def attach(self, obs):
        self.observers.append(obs)

    def detach(self, obs):
        self.observers.remove(obs)

    def notify(self, msg):
        for obj in self.observers:
            obj.update(msg)


class KafkaReader(Reader):
    def __init__(self, hosts: str, topic_name: str, zk_hosts: str = ZK_HOSTS):
        super().__init__()
        self.hosts = hosts
        self.topic_name = topic_name
        self.zk_hosts = zk_hosts
        self.client = KafkaClient(hosts=hosts)
        self.topic = self.client.topics[topic_name]

    def read(self):
        message = None

        balanced_consumer = self.topic.get_balanced_consumer(
            consumer_group=f'{self.topic_name}_group',
            auto_commit_enable=True,
            zookeeper_connect=self.zk_hosts
        )

        try:
            for message in balanced_consumer:
                if message is not None:
                    # self.notify((message.offset, message.value))
                    self.notify(message)
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
            return '', []

        if not keys:
            keys = list(data.keys())

        if not columns:
            columns = self.columns or keys

        sql = self.sql if columns == self.columns else self.build(columns)
        values = [[data.get(k) for k in keys] for data in datas if data]

        return sql, values


class Observer(metaclass=ABCMeta):
    @abstractmethod
    def update(self, msg):
        pass


class Consumer(Observer):
    router_table = {
        'insert': ('insert', 'bootstrap-insert'),
        'update': ('update',),
        'delete': ('delete',),
        'table-alter': ('alter table',),
    }

    def __init__(self, database, table, columns=None, mode=None, keys=None):
        """\
        处理 reader 产生的数据，写入目标库
        :param database: 写入目标数据库, str
        :param table: 写入目标数据表, str
        :param columns: 写入目标数据表的字段，[]
        :param mode: 写入目标库的模式, str
        :param keys: 用户读取 reader 产生的数据的key,[]
        """
        self.q = Queue(50_000)
        # 'bootstrap-insert' 类型的消息会顺势产生大量数据，需要一个穿冲队列
        self.insert_buffer = []
        # 缓冲队列最大值
        self.max_buf_size = 5_000

        # todo: 先获取上次的 offset
        self.offset = 0
        # 初始化 sql 构造器
        self.builder = SQLBuilder(database, table, columns, mode)
        # 用于 sql 构造器中从数据源抽取数据
        self.keys = keys

        # 数据库连接
        self.db = MySQLDBHelper(**CONFIG.get(database))

        # 子线程与主线程通信的队列
        # todo: 是不是应该使用线程池的方式
        self.tasks = Queue(10)
        # 表示主线程处理的当前任务
        self.current = None
        # 主线程循环结束标志位
        self.term_flag = False
        # 初始子线程并启动
        self.worker = Thread(target=self.start, daemon=True)
        self.worker.start()

    def update(self, msg):
        self.q.put(msg)

    def start(self):
        """子线程负责从队列获取数据，然后放入缓冲队列，以及刷新队列生成提交任务"""
        timeout = 5
        while True:
            try:
                msg = self.q.get(timeout=timeout)
            except Empty:
                self.flush()
                timeout = min(timeout + 5, 60)
            else:
                timeout = 5
                flush_flag = self.route(msg)
                # 根据路由结果和等待时间确定是否刷新
                # 如果路由结果=true: 表示超过缓存队列
                # 等待时间确定>5: 表示当前消息队列负载很低
                if flush_flag or timeout > 5:
                    self.flush()
                    self.offset = msg.offset
                    # todo: offset 保存至 zookeeper 上每消费一条数据更新一次

    def route(self, message):
        """对 message 进行路由处理"""
        if not message:
            return True

        value = message.value
        action_type = value.get('type')
        if action_type in self.router_table['insert']:
            data = value.get('data')
            self.insert_buffer.append(data)

        return len(self.insert_buffer) >= self.max_buf_size

    def flush(self):
        """刷新队列"""
        if self.insert_buffer:
            sql, values = self.builder.insert(self.insert_buffer, self.keys)
            if all((sql, values)):
                self.tasks.put(Thread(target=self.execute, args=(sql, values)))
            self.insert_buffer = []

    def run(self):
        """主线程负责执行子线程生成的任务"""
        signal.signal(signal.SIGTERM, self._term_handler)
        signal.signal(signal.SIGINT, self._term_handler)

        while not self.term_flag:
            try:
                self.current = self.tasks.get()
                self.current.start()
                self.current.join()
            except KeyboardInterrupt:
                if self.current and self.current.isAlive():
                    self.current.join()
                break

    def _term_handler(self, signal_num, frame):
        """系统信号量处理"""
        self.term_flag = True
        if self.current and self.current.isAlive():
            self.current.join()
        exit(1)

    def execute(self, sql, args):
        """执行 sql"""
        result = None
        try:
            result = self.db.executemany(sql, args)
        except Exception as e:
            print(e)
            self.db.rollback()
        else:
            self.db.commit()
        # todo: offset 保存, 每消费一条数据更新一次
        return result


class Message:
    def __init__(self, offset, value):
        self.offset = offset
        self.value = value


if __name__ == '__main__':
    # kafka = KafkaReader(HOSTS, 'ns_alluser_xinyongfei_cs_StarUser')

    d, t = 'shoufuyou_statistics', 'StarUser'
    v1 = {
        "database": "shoufuyou_v2",
        "table": "User",
        "type": "bootstrap-insert",
        "ts": 15583311111,
        "data": {
            "id": 1,
            "mobile": "15868112222",
            "created_time": "2019-05-18 17:59:59",
            "gender": "other",
            "utm_source": "小白信用分",
            "updated_time": "2019-05-18 17:59:59",
            "app_source": "",

        }
    }
    v2 = {
        "database": "shoufuyou_v2",
        "table": "User",
        "type": "bootstrap-insert",
        "ts": 1558332314,
        "data": {
            "mobile": "15868113333",
            "created_time": "2019-05-19 17:59:59",
            "gender": "other",
            "utm_source": "大白信用分",
            "updated_time": "2019-05-19 17:59:59",
            "app_source": "",

        }
    }
    # consumer = Consumer(d, t)
    #
    # msg1 = Message(1, v1)
    # consumer.update(msg1)
    #
    # msg1 = Message(2, v2)
    # consumer.update(msg1)
    #
    # consumer.run()

    # db = MySQLDBHelper(**DB_DEFAULT_CONFIG)
    #
    # r = db.execute("set wait_timeout=10;")
    # r = db.execute("set interactive_timeout=10;")
    # r = db.execute("select * from StarUser;")
    # values = db.cr.fetchall()    or []
    # print(values)
    #
    # # time.sleep(15)
    #
    # sql = """insert into `shoufuyou_statistics`.`StarUser`
    # (mobile,created_time,gender,utm_source,updated_time,app_source)
    # values (%s,%s,%s,%s,%s,%s);"""
    # args = (
    #     ('15583311111', '2019-05-18 17:59:59', 'other', '小白信用分', '2019-05-18 17:59:59', ''),
    #     ('15868112315', '2019-05-19 17:59:59', 'other', '大白信用分', '2019-05-19 17:59:59', '')
    # )
    #
    # r = db.executemany(sql, args)
    # db.commit()
    # r = db.execute("select * from StarUser;")
    # values = db.cr.fetchall() or []
    # print(values)
    #
    # db.close()
    # db.close()
