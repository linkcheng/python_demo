#!/usr/bin/env python

def func1(i, data = []):
    print 'type(data) = %s' % type(data)
    data.append(i)
    return data

def func2(i, data = None):
    print 'type(data) = %s' % type(data)
    if data is None:
        data = []
    data.append(i)
    return data

sentinel = object()
def func3(i, data = sentinel):
    print 'type(data) = %s' % type(data)
    if data is sentinel:
        data = []
    data.append(i)
    return data

for i in range(3):
    ret = func1(i)
    print 'func1(%d) = ' % i,
    print ret

    ret = func2(i)
    print 'func2(%d) = ' % i,
    print ret

    ret = func3(i)
    print 'func3(%d) = ' % i,
    print ret
