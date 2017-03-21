# -*- coding: utf-8 -*-


def make_counter():
    count = 0

    def counter():
        nonlocal count  # use python 3
        count = 1
        print(count)
        return count
    print(count)
    return counter

var = 0

def func(num):
    print(num)
    func.var = var # func.var is referring the local
                   # variable var inside the function func
    if num != 0:
        func(num-1)


count = make_counter()
count()
# func(10)
