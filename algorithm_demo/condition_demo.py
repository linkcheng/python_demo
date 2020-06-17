#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author: Link 
@module: condition_demo 
@date: 2020-06-15 
"""
from typing import Sequence
import threading
from threading import Thread, Condition


class A(Thread):
    def __init__(self, name: str, cond: Condition, data: Sequence):
        super().__init__(name=name)
        self.cond = cond
        self.data = data

    def run(self):
        for item in self.data:
            with self.cond:
                self.cond.wait()
                print(item)
                threading.local()
                self.cond.notify()


class B(Thread):
    def __init__(self, name: str, cond: Condition, data: Sequence):
        super().__init__(name=name)
        self.cond = cond
        self.data = data

    def run(self):
        for item in self.data:
            with self.cond:
                print(item)
                self.cond.notify()
                self.cond.wait()


if __name__ == '__main__':
    c = Condition()
    a_data = '0,1,2,3,4,5,6,7,8,9'.split(',')
    a = A('A', c, a_data)
    b_data = 'a,b,c,d,e,f,g,h,i,j,k,l'.split(',')
    b = B('B', c, b_data)

    a.start()
    b.start()
