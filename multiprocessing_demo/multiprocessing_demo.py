#!/usr/bin/env python
# coding:utf-8  
# @Author: linkcheng
# function：get commit id and files' url

import time
import os
from multiprocessing import Process, Queue  
from functools import wraps
  
def fn_timer(function):
    @wraps(function)
    def function_timer(*args, **kwargs):
        start = time.time()
        result = function(*args, **kwargs)
        end = time.time()
        
        print ("Total time running %s: %s seconds" % (function.func_name, str(end-start)))
        return result
        
    return function_timer

@fn_timer
def offer1(queue, i):
    print "subproc1 id = %d" % os.getpid()  
    time.sleep(i)  
    queue.put("Hello World i = %d" % i)
  
@fn_timer
def offer2(queue, i):  
    l = [i, "Hello World"]
    print "subproc2 id = %d" % os.getpid()
    time.sleep(i)  
    queue.put(l)

if __name__ == '__main__':  
    q = Queue()
    
    p = Process(target=offer1, args=(q, 5))  
    p1 = Process(target=offer2, args=(q, 2))  
    
    p.start()
    p1.start()
    
    print "main id = %d" % os.getpid()    
    get1 = q.get()
    get2 = q.get()
    
    print type(get1)
    print type(get2)

