#! /usr/bin/env python
# -*- coding: utf-8 -*-

import time
from functools import wraps
import threading

def fn_timer(function):
    """
    计算 function 的运算时间
    :param function:
    :return:
    """
    @wraps(function)
    def function_timer(*args, **kwargs):
        start = time.time()
        result = function(*args, **kwargs)
        end = time.time()

        print('Total time running %s: %s seconds' % (function.func_name, str(end - start)))
        return result

    return function_timer


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
    # 把StringIO的写函数注册到pycurl的WRITEFUNCTION中，即pycurl所有获取的内容都写入到StringIO中，如果没有这一句，pycurl就会把所有的内容在默认的输出器中输出
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
        datetime.strptime(date, "%Y-%pattern-%d")
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


def binary_search(array, key):
    left = 0
    right = len(array) - 1

    while left <= right:
        mid = (left + right) / 2

        if key == array[mid]:
            return mid
        elif key > array[mid]:
            left = mid + 1
        else:
            right = mid - 1

    return -1


class ChineseCapitalForm(object):
    measure = cdict = {1: u'', 2: u'拾', 3: u'佰', 4: u'仟'}
    unit = xdict = {1: u'元', 2: u'万', 3: u'亿', 4: u'兆'}
    chn = gdict = {'0': u'零', '1': u'壹', '2': u'贰', '3': u'叁', '4': u'肆',
                   '5': u'伍', '6': u'陆', '7': u'柒', '8': u'捌', '9': u'玖'}

    @staticmethod
    def split_num(num_str):
        """拆分函数，将整数字符串拆分成[亿，万，仟]的list"""

        num_list = []
        i = len(num_str) % 4
        len_num = len(num_str) - 1

        if i > 0:
            num_list.append(num_str[:i])

        while i <= len_num:
            num_list.append(num_str[i: i+4])
            i += 4
        return num_list

    def translate_num(self, num_str):
        """对[亿，万，仟]的list中每个字符串分组进行大写化再合并"""

        len_num = len(num_str)
        capital = u''
        for i, num in enumerate(num_str):
            if num == '0':
                # 如果i不是最后一位并且i下一位不是0
                if i < len_num-1 and num_str[i+1] != '0':
                    capital += self.chn[num_str[i]]
            else:
                capital = capital + self.chn[num_str[i]] + self.measure[len_num-i]
        return capital

    def transform(self, numeral):
        """转换数字为大写中文"""

        integer_num_str, decimal_num_str = str(numeral).split('.')
        capital = u''

        # 分解字符数组[亿，万，仟]三组List:['0000','0000','0000']
        integer_num_list = self.split_num(integer_num_str)

        # 获取拆分后的List长度，大写合并
        for i, num_str in enumerate(integer_num_list):
            # 有可能一个字符串全是0的情况
            tmp = self.translate_num(num_str)
            capital += tmp
            if tmp:
                # 合并：前字符串大写+当前字符串大写+标识符
                capital += self.unit[len(integer_num_list)-i]

        # 处理小数部分
        if len(decimal_num_str) == 1:  # 若小数只有1位
            if int(decimal_num_str[0]) == 0:
                capital += u'整'
            else:
                capital = capital + self.chn[decimal_num_str[0]] + u'角整'
        else:  # 若小数有两位的四种情况
            tenths, percentile = decimal_num_str[0], decimal_num_str[1]
            if tenths == '0' and percentile != '0':
                capital = capital + u'零' + self.chn[percentile] + u'分'
            elif tenths == '0' and percentile == '0':
                capital += u'整'
            elif tenths != '0' and percentile != '0':
                capital = capital + self.chn[tenths] + u'角' + self.chn[percentile] + u'分'
            else:
                capital = capital + self.chn[tenths] + u'角整'
        return capital


@fn_timer
def test_fibonacci_recursive(n):
    print fibonacci_recursive(n)


@fn_timer
def test_fibonacci(n):
    print fibonacci(n)


def fibonacci(n):
    cur, nxt = 0, 1

    for i in range(n):
        cur, nxt = nxt, cur + nxt

    return cur


def fibonacci_recursive(n):
    if n <= 0:
        return 0

    return 1 if n == 1 else fibonacci_recursive(n-1) + fibonacci_recursive(n-2)


def test_f():
    ts = []

    t1 = threading.Thread(target=test_fibonacci, args=(30,), name='test_fibonacci')
    t1.setDaemon(True)
    ts.append(t1)

    t2 = threading.Thread(target=test_fibonacci_recursive, args=(30,), name='test_fibonacci_recursive')
    t2.setDaemon(True)
    ts.append(t2)

    for t in ts:
        t.start()

    for t in ts:
        t.join()


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

    # curl_test()

    # print(binary_search(range(100), 13))

    # pt = ChineseCapitalForm()
    # print pt.transform('600190101000.80')

    test_f()


if __name__ == '__main__':
    main()
