# -*- encoding: utf-8 -*-
import time
import threading
from conn_odoo import config
from parameters import before_sql, before_uninstall_modules
from method import GoLiveMethod

ERROR_NUM = 0
ERROR_DICT = {}


def do_works(section):
    # 实例化连接
    thread = GoLiveMethod(section)

    # 1、升级前执行SQL语句 overwrite=True
    thread.execute_sql(before_sql)

    # 2、卸载模块
    thread.uninstall_modules(before_uninstall_modules)

if __name__ == '__main__':
    t1 = time.time()
    Threads = []
    sections = config.sections()
    # 创建线程
    for section in sections:
        t = threading.Thread(target=do_works, args=(section,), name=section)
        t.setDaemon(True)
        Threads.append(t)

    for t in Threads:
        t.start()

    for t in Threads:
        t.join()

    print "All ended!"

    t2 = time.time()

    print "========================================"
    print "总耗时(秒):", t2 - t1
    print "平均耗时(秒):", (t2 - t1) / len(sections)
    print "错误步骤数量:", ERROR_NUM
    print "错误详情:", ERROR_DICT



