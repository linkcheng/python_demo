#! /usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import time
import hashlib
import gevent
import threading
from functools import wraps


def fn_timer(function):
    @wraps(function)
    def function_timer(*args, **kwargs):
        start = time.time()
        result = function(*args, **kwargs)
        end = time.time()
        print('Total time running %s: %s seconds' % (function.func_name, str(end - start)))
        # info_logger.info('Total time running %s: %s seconds' % (function.func_name, str(end - start)))
        return result

    return function_timer


def alidayu_sms_test():
    import top.api

    appkey = "appkey"
    secret = "secret"
    req = top.api.AlibabaAliqinFcSmsNumSendRequest()
    req.set_app_info(top.appinfo(appkey, secret))

    req.sms_type = "normal"
    req.rec_num = "****"
    req.sms_template_code = "****"
    req.sms_free_sign_name = "风轻扬"
    req.sms_param = {"name": "Link", "number": "123456"}
    resp = req.getResponse()
    print(resp)


def netease_sms_test():
    url = 'https://api.netease.im/sms/sendtemplate.action'
    app_key = 'bfa97845976c6680921e8874b368ce19'
    app_secret = '58fafa116b75'

    cur_time = str(long(time.time()))
    nonce = get_nonce(cur_time)
    check_sum = get_checksum(app_secret, nonce, cur_time)

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'charset': 'utf-8',
        'AppKey': app_key,
        'CurTime': cur_time,
        'CheckSum': check_sum,
        'Nonce': nonce,
    }

    data = {
        'templateid': 3056140,
        'mobiles': '["17092100248"]',
        'params': "['123456', '30']",
    }

    ret = requests.post(url, headers=headers, data=data)

    print(ret.content.json)


def get_nonce(pstr):
    return hashlib.md5(pstr).hexdigest()


def get_checksum(app_secret, nonce, cur_time):
    return hashlib.sha1(app_secret + nonce + cur_time).hexdigest()


def consumer():
    r = ''
    while True:
        n = yield r
        if not n:
            return
        print('consuming the event %s' % n)
        r = '200 OK'


def produce(c):
    # c.send(None)
    for n in range(1, 6):
        c.send(None)
        print('producing event %s' % n)
        r = c.send(n)
        print('the consumer response %s' % r)

    c.close()


def task1():
    print('====== task 1 start ========\n')
    gevent.sleep(1)
    print('====== task 1 over ========')


def task2():
    print('====== task 2 start ========\n')
    gevent.sleep(2)
    print('====== task 2 over ========')


def thread_routine():
    print('====== thread routine start ========\n')
    gevent.joinall([
        gevent.spawn(task1),
        gevent.spawn(task2),
    ])
    time.sleep(60)
    print('====== thread routine over ========')


@fn_timer
def main_routine():
    """
    线程不设置 setDaemon 与 join：主线程结束不等待子线程，也不会杀死子线程而是自由运行
    因为没有设置 join，故主线程不等待子线程，
    因为没有设置 setDaemon(True)，即主进程没有设置为守护进程，故主线程结束不会杀死子线程，但程序会被无限挂起，直到所有线程结束才结束
        ========= main process start =======
        ====== main routine start ========
        ====== thread routine start ========

        ====== main routine over ========
        Total time running main_routine: 0.00149011611938 seconds
        ========= main process over ========
        ====== task 1 start ========

        ====== task 2 start ========

        ====== task 1 over ========
        ====== task 2 over ========
        ====== thread routine over ========

    线程设置 setDaemon，不设置join：主线程不等待子线程，主线程结束就会杀死子线程，程序结束
        ========= main process start =======
        ====== main routine start ========
        ====== thread routine start ========
        ====== main routine over ========

        Total time running main_routine: 0.000439882278442 seconds
        ========= main process over ========

    线程不设置 setDaemon，设置 join： 即主线程阻塞，等待子线程结束
        ========= main process start =======
        ====== main routine start ========
        ====== thread routine start ========

        ====== task 1 start ========

        ====== task 2 start ========

        ====== task 1 over ========
        ====== task 2 over ========
        ====== thread routine over ========
        ====== main routine over ========
        Total time running main_routine: 2.00796294212 seconds
        ========= main process over ========

    线程设置 setDaemon 与 join： 其实是只起到 join 的作用，即主线程阻塞，等待子线程结束，
        ========= main process start =======
        ====== main routine start ========
        ====== thread routine start ========

        ====== task 1 start ========

        ====== task 2 start ========

        ====== task 1 over ========
        ====== task 2 over ========
        ====== thread routine over ========
        ====== main routine over ========
        Total time running main_routine: 2.00859498978 seconds
        ========= main process over ========
    :return:
    """

    print('====== main routine start ========')
    t = threading.Thread(target=thread_routine, name='sms_test_thread_routine_with_gevent')
    # t.setDaemon(True)
    t.start()
    # t.join()
    print('====== main routine over ========\n')


if __name__ == '__main__':
    print('========= main process start =======')
    # netease_sms_test()
    # c = consumer()
    # produce(c)
    main_routine()
    time.sleep(30)
    print('========= main process over ========')
