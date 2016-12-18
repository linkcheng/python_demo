def fib(n):
    index = 0
    a = 0
    b = 1
    while index < n:
        yield b
        a, b = b, a + b
        index += 1

for fi in fib(20):
    print(fi)


def lazy_fib(n):
    index = 0
    a = 0
    b = 1
    while index < n:
        s = yield b
        print(s)
        a, b = b, a + b
        index += 1

l = lazy_fib(20)
l.next()     #==l.send(None)
l.send(2)

def copy_fib(n):
    print("copy_fib")
    yield from fib(n)
    print("end copy")

for c in copy_fib(20):
    print(c)


import asyncio
import random

@asyncio.coroutine
def smart_fib(n):
    index = 0
    a = 0
    b = 1
    while index < n:
        sleep_secs = random.uniform(0, 0.2)
        yield from asyncio.sleep(sleep_secs)
        print('Smart one think {} secs to get {}'.format(sleep_secs, b))
        a, b = b, a + b
        index += 1
 
@asyncio.coroutine
def stupid_fib(n):
    index = 0
    a = 0
    b = 1
    while index < n: 
        sleep_secs = random.uniform(0, 0.4)
        yield from asyncio.sleep(sleep_secs)
        print('Stupid one think {} secs to get {}'.format(sleep_secs, b))
        a, b = b, a + b
        index += 1
 

loop1 = asyncio.get_event_loop()
tasks1 = [
    asyncio.async(smart_fib(10)),
    asyncio.async(stupid_fib(10)),
]
loop1.run_until_complete(asyncio.wait(tasks1))
print('All fib finished.')
loop1.close()
