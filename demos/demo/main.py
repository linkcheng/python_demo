# -*- coding: utf-8 -*-
# !/usr/bin/python


def my_sqrt_test():
    import my_sqrt

    my_sqrt.my_sqrt(244000)
    my_sqrt.math_sqrt(244000)


def reverse_sentense_test():
    import reverse_sentense
    res = reverse_sentense.reverse_sentense('the sky is blue')
    print('reverse \'the sky is blue\' = %s' % res)


def compare_str_test():
    # T=acaabc 和模式P=aab
    import compare_str

    text = 'asdfghjklqwertyuiopzxcvbnmqwertyuiopasdfghjklzxcvbnmqwertyuiop'
    pattern = 'asdfghjklzxcvbnm'

    res1 = compare_str.compare_str(text, pattern)
    print(res1)
    res2 = compare_str.compare_str_2(text, pattern)
    print(res2)


def max_subarray_test():
    import maximum_subarray
    a = [1, -2, 2, 2, 3, 1, -1, 2, -1]
    res = maximum_subarray.max_subarray(a)
    print(res)


def g_test():
    import yield_demo
    f = yield_demo.g()
    print(f.next())
    print(f.send(5))
    f.send(2)


def max_subarray(A):
    max_ending_here = max_so_far = 0
    for x in A:
        max_ending_here = max(0, max_ending_here + x)
        max_so_far = max(max_so_far, max_ending_here)
    return max_so_far


def gevent_test():
    import gevent_demo
    gevent_demo.demo_run()


def main():
    # my_sqrt_test()
    # reverse_sentense_test()
    # compare_str_test()
    # max_subarray_test()
    # g_test()
    gevent_test()

if '__main__' == __name__:
    main()
