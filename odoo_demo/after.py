# -*- encoding: utf-8 -*-
import time
import threading
from conn_odoo import config
from parameters import after_sql, after_install_modules, after_update_modules, after_uninstall_modules, after_function_tools, after_load_files
from method import GoLiveMethod

ERROR_NUM = 0
ERROR_DICT = {}


def do_works(section):
    # 实例化连接
    thread = GoLiveMethod(section)

    # 1、升级模块
    thread.update_modules(after_update_modules)

    # 2、安装模块
    thread.install_modules(after_install_modules)

    # 3、卸载模块
    thread.uninstall_modules(after_uninstall_modules)

    # 4、升级后执行SQL语句
    thread.execute_sql(after_sql)

    # 5、加载指定数据文件
    thread.load_files(after_load_files)

    # 6、加载系统翻译
    thread.load_translation()

    # 7、运行function tool函数
    thread.run_function_tool(after_function_tools)


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

