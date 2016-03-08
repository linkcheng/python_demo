#!/usr/bin/env python

from contextlib import contextmanager

@contextmanager
def demo():
    print '[Allocate resource]'
    print 'Code before yield-statement executes in __enter__'
    yield '*** contextmanager demo ***'
    print 'Code after yield-statement executes in __exit__'
    print '[Free resource]'

with demo() as value:
    print 'Assigned value: %s' % value
