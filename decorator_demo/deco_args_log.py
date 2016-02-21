#import os,sys
#from time import ctime,sleep,time
from time import time
#import codecs
#import re

def logged(when):
    def log(f,*args,**kargs):
        print '''called:function:%s args:%r kargs:%r''' % (f,args,kargs)
                
    def pre_logged(f):
        def wrapper(*args,**kargs):
            log(f,*args,**kargs)
            return f(*args,**kargs)
        return wrapper
                                                        
    def post_logged(f):
        def wrapper(*args,**kargs):
            now = time()
            try:
                return f(*args,**kargs)
            finally:
                log(f,*args,**kargs)     
                print 'time delta:%s' % (time()-now)
        return wrapper

    try:
        return {'pre':pre_logged,'post':post_logged}[when] # return the function arg of when representative
    except KeyError as e:
        print 'must be pre or post'
                                         
@logged('post')
def hello(name):
    print'Hello,%s' % name

hello('world')
