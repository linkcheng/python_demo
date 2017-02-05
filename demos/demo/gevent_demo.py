# -*- coding: utf-8 -*-
import gevent
from gevent.event import Event, AsyncResult


evt = AsyncResult()


def setter():
    print('好好听课')
    gevent.sleep(5)  # 持续时间为5
    print('好的 ,下课')
    global evt
    evt.set('hello world')


def waiter():  # 等待下课
    print('听课...')
    global evt, is_ok
    data = evt.get()
    print(data)
    print('哈哈 , 终于下课了')


def demo_run():
    gevent.joinall([
        gevent.spawn(setter),
        # gevent.spawn(waiter),
        gevent.spawn(waiter)
    ])
