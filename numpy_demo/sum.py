#!/usr/bin/env/python
import sys
from datetime import datetime
import numpy as np

def pythonsum(n):
    a = range(n)
    b = range(n)
    c = []

    for i in range(len(a)):
        a[i] = i ** 2
        b[i] = i ** 3
        c.append(a[i] + b[i])

    return c

def numpysum(n):
    a = np.arange(n) ** 2
    b = np.arange(n) ** 3
    c = a + b

    return c

if __name__ == '__main__':
    size = int(sys.argv[1])

    start = datetime.now() 
    c = pythonsum(size)
    delta = datetime.now()  - start
    print "The last 2 elements of the sum" , c[-2:]
    print "PythonSum elapsed time in microseconds", delta.microseconds, "\n"

    start = datetime.now() 
    c = numpysum(size)
    delta = datetime.now()  - start
    print "The last 2 elements of the sum" , c[-2:]
    print "NumpySum elapsed time in microseconds", delta.microseconds, "\n"
