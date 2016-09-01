#! /usr/bin python

import os
import time
import random
import threading
from multiprocessing import Process, Queue  
from functools import wraps

def fn_timer(function):
    @wraps(function)
    def function_timer(*args, **kwargs):
        start = time.time()
        result = function(*args, **kwargs)
        end = time.time()
        print('In %s process, total time running %s: %s seconds\n' % (os.getpid(), function.func_name, str(end - start)))
        return result
    return function_timer

results = 1
lock = threading.Lock()

def product(seqs):
    ans = 1
    for seq in seqs:
        ans *= seq
    return ans

def cal_proc_product(seqs):
    global results
    part_answer = product(seqs)
    lock.acquire()
    results *= part_answer
    lock.release()

def cal_proc_sum(seqs):
    global results
    part_answer = sum(seqs)
    lock.acquire()
    results += part_answer
    lock.release()

@fn_timer
def cal_sum(seqs, queue = None):
    if queue is None: #single process
        cal_proc_sum(seqs)
    else: #multi process
        part_answer = sum(seqs)
        queue.put(part_answer)

@fn_timer
def cal(seqs, queue = None):
    if queue is None: #single process
        cal_proc_product(seqs)
    else: #multi process
        part_answer = product(seqs)
        queue.put(part_answer)

@fn_timer
def single_cal(data):
    ''' get sum in single thread'''
    global results
    results = 1
    cal(data)
    # print(results)

@fn_timer
def multi_cal(jobs):
    '''get sum in multi thread'''
    global results
    results = 1
    for job in jobs:
        job.start()
    # print(results)

@fn_timer
def single_thread(data):
    single_cal(data)

@fn_timer
def multi_thread(data):
    jobs = []
    while data:
        part, data = data[:2**17], data[2**17:]
        jobs.append(threading.Thread(target=cal, args=(part, )))
    multi_cal(jobs)

@fn_timer
def multi_process(data):
    global results
    results = 1
    jobs = []
    q = Queue()

    while data:
        part, data = data[:2**17], data[2**17:]
        jobs.append(Process(target=cal, args=(part, q)))

    for job in jobs:
        job.start()

    for job in jobs:
            get_part_ans = q.get()
            results *= get_part_ans

    # print(results)


@fn_timer
def main():
    data = [random.randint(1, 3) for i in range(2**20)]

    single_thread(data)

    multi_thread(data)

    multi_process(data)

if "__main__" == __name__:
    main()
