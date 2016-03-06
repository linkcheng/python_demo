#!/usr/bin/env python
# coding=utf-8

print 'running start'
with open(r'/tmp/mytmp/hello.tmp') as somefile:
    for line in somefile:
        print line,
print 'running end\n'

print '============================================'

class DummyResource:
    def __init__(self, tag):
        self.tag = tag
        print 'Resource [%s]' % tag
    def __enter__(self):
        print '[Enter %s]: Allocate resource.' % self.tag
        return self   # can return is not context manager 
    def __exit__(self, exc_type, exc_value, exc_tb):
        print '[Exit %s]: Free resource.' % self.tag
        if exc_tb is None:
            print '[Exit %s]: Exited without exception.' % self.tag
        else:
            print '[Exit %s]: Exited with exception raised.' % self.tag
        return False   # return is not necessary，None is as same as False

with DummyResource('normal') as dr:
    print '[with body] run without exception tag = %s' % dr.tag

print '============================================'

