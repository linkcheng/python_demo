#!/usr/bin/env python

def decor(start):
    def _deco(func):
        def deco(*args, **kwargs):
            print "before decorator! start = %s" % (start)
            func(start, *args, **kwargs)
            print "after decorator!\n"
        return deco
    return _deco
    

@decor("mymodule")
def runFun(*args, **kwargs):
    print "This is run method!, args = %s, kwargs = %s" % (args, kwargs)

if __name__ == "__main__":
    runFun(1, 2)   # runFun(1, 2) = decor("mymodule")(runFun)(1, 2) => _deco(runFun)(1, 2) => deco(1, 2)
    runFun(3, 4, m=5, n=6)
