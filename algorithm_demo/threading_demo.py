#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author: Link 
@module: threading_demo 
@date: 2020-06-23 
"""
import threading
import os
import time


def fun():
    p = os.fork()
    if p == 0:
        print(f"this is child, {os.getpid()}, {threading.get_ident()}")
        time.sleep(30)
    else:
        print(f"this is parent, {os.getpid()}, {threading.get_ident()}")
        time.sleep(30)


t = threading.Thread(target=fun)


t.start()
print(f'{os.getpid()}, {threading.get_ident()}')
t.join()
