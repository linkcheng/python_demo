# -*- coding: utf-8 -*-
import time
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
