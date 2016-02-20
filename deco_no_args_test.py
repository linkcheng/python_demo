#!/usr/bin/env python

def decor(start):
    def deco(*args, **kwargs):
        print "before decorator!"
        start(*args, **kwargs)
        print "after decorator!\n"
    return deco
    

@decor
def runFun(*args, **kwargs):
    print "This is run method!, args = %s, kwargs = %s" % (args, kwargs)

if __name__ == "__main__":
    runFun(1, 2, x=3, y=4)
    runFun(3, 4, m=5, n=6)
