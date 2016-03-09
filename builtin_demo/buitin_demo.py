#!/usr/bin/env python 


print '361! =',

i = reduce(lambda x, y: x*y, range(1, 362))

print i

s = str(i)

print 'len(361!) = %s' % len(s)

