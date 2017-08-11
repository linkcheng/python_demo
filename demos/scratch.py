#! /usr/bin/env python
# -*- coding: utf-8 -*-


def gettext_test():
    import locale
    import gettext

    current_locale, encoding = locale.getdefaultlocale()
    locale_path = 'po'

    # zh_trans = gettext.translation('scratch', locale_path, languages=['zh_CN'])
    # en_trans = gettext.translation('scratch', locale_path, languages=['en_US'])

    trans = gettext.translation('scratch', locale_path)

    _ = trans.gettext
    trans.install()
    print(_('Hello world!'))
    print(_('Python is a good language'))


def redis_test():
    import redis

    # r = redis.StrictRedis(host='localhost', port=6379, db=0)

    # 创建连接池，默认一个实例一个连接池
    pool = redis.ConnectionPool(host='localhost', port=6379, db=0)
    r = redis.Redis(connection_pool=pool)

    try:
        r.set('foo', 'bar')
        print('set foo')
        return True
    finally:
        print('get foo = %s' % r.get('foo'))


def celery_test():
    from celery import Celery
    from kombu import Exchange, Queue

    CELERY_QUEUES = (
        Queue('default', Exchange('default'), routing_key='default'),
        Queue('for_task_A', Exchange('for_task_A'), routing_key='for_task_A'),
        Queue('for_task_B', Exchange('for_task_B'), routing_key='for_task_B'),
    )

    CELERY_ROUTES = {
        'my_taskA': {'queue': 'for_task_A', 'routing_key': 'for_task_A'},
        'my_taskB': {'queue': 'for_task_B', 'routing_key': 'for_task_B'},
    }

    app = Celery('tasks', backend='redis://localhost', broker='redis://localhost')

    @app.task
    def add(x, y):
        return x + y


def curl_test():
    import StringIO
    import pycurl

    c = pycurl.Curl()
    b = StringIO.StringIO()
    c.setopt(pycurl.URL, "http://t.cn/aKln8T")
    c.setopt(pycurl.WRITEFUNCTION, b.write)
    c.setopt(pycurl.FOLLOWLOCATION, 1)

    c.perform()
    print c.getinfo(pycurl.EFFECTIVE_URL)


import time, sched

# 实例化一个sched对象
schedule = sched.scheduler(time.time, time.sleep)


def execute_operate(inc):
    # do something
    print('----')
    schedule.enter(inc, 0, execute_operate, [inc])
    pass


def main_start(inc=1):
    schedule.enter(0, 0, execute_operate, [inc])
    schedule.run()


class hello:
    def GET(self):
        return 'Hello, World'


def web_test():
    import web

    urls = (
        '/', 'hello'
    )

    app = web.application(urls, globals())
    app.run()


def selenium_test():
    from selenium import webdriver
    from selenium.webdriver.common.keys import Keys
    import time
    # selenium.common.exceptions.WebDriverException: Message: 'chromedriver' executable needs to be in PATH.
    # Please see https://sites.google.com/a/chromium.org/chromedriver/home
    # 下载 chromedriver，并且放到 PATH 目录下

    driver = webdriver.Chrome()
    driver.get('http://www.baidu.com/')
    elem = driver.find_element_by_name("q")
    elem.send_keys("pycon")
    elem.send_keys(Keys.RETURN)

    print(driver.page_source)
    time.sleep(30)


def is_valid_date(date):
    """
    判断是否是一个有效的日期字符串
    """
    from datetime import datetime
    try:
        datetime.strptime(date, "%Y-%m-%d")
        return True
    except Exception:
        return False


def qrcode_test():
    import qrcode

    qr = qrcode.QRCode(
        version=2,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=1
    )
    qr.add_data("http://192.168.0.66:48069")
    qr.make(fit=True)
    img = qr.make_image()
    img.save("localhost_qrcode.png")


def account_email():
    emails = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    accounts = ['a', 'b']

    len_account = len(accounts)

    for index, account in enumerate(emails):
        print account, accounts[index % len_account]

    l = [(account, accounts[index % len_account]) for index, account in enumerate(emails)]
    print l


def mongo_test():
    import pymongo
    # 建立连接
    clinet = pymongo.MongoClient("localhost", 27017)
    # 获取数据库
    db = clinet["PornHub"]
    # 连接集合（表）
    table = db["PhRes"]
    records = table.find({})
    for record in records:
        print(record)


def tensorflow_test():
    import tensorflow as tf
    hello = tf.constant('Hello, TensorFlow!')
    sess = tf.Session()
    print(sess.run(hello))


def main():
    # gettext_test()

    # redis_test()

    # celery_test()

    # main_start()

    # web_test()

    # selenium_test()

    # qrcode_test()

    # account_email()

    # mongo_test()

    # tensorflow_test()

    curl_test()

if __name__ == '__main__':
    main()
