#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
import asyncio
import aiohttp
import uvloop
import time
import socket
from selectors import DefaultSelector, EVENT_READ, EVENT_WRITE
from datetime import datetime


async def async_http_test():
    url = 'http://bi-service.xyf.cn/api'
    async with aiohttp.request('GET', url) as r:
        data = await r.json()
        # print(data)
    return data


selector = DefaultSelector()
stopped = False
urls_todo = ['/', '/', '/']


class Crawler(object):
    def __init__(self, url):
        self.url = url
        self.sock = None
        self.response = b''

    def fetch(self):
        self.sock = socket.socket()
        self.sock.setblocking(False)
        try:
            self.sock.connect(('www.baidu.com', 443))
        except BlockingIOError:
            pass
        selector.register(self.sock.fileno(), EVENT_WRITE, self.connected)

    def connected(self, key, mask):
        selector.unregister(key.fd)
        get = 'GET HTTP/1.0\r\nHost://www.baidu.com\r\n\r\n'
        self.sock.send(get.encode('ascii'))
        selector.register(key.fd, EVENT_READ, self.read_response)

    def read_response(self, key, mask):
        global stopped
        chunk = self.sock.recv(4096)
        if chunk:
            self.response += chunk
            print(self.response)
        else:
            selector.unregister(key.fd)
            urls_todo.remove(self.url)
            if not urls_todo:
                stopped = True


def loop():
    while not stopped:
        events = selector.select()
        for event_key, event_mask in events:
            callback = event_key.data
            callback(event_key, event_mask)


if __name__ == '__main__':
    # uvloop
    start = time.time()
    loop = uvloop.new_event_loop()
    asyncio.set_event_loop(loop)
    tasks = [async_http_test() for _ in range(800)]
    results = loop.run_until_complete(asyncio.gather(*tasks))
    print(time.time() - start)

    # default loop
    start = time.time()
    loop1 = asyncio.get_event_loop()
    tasks = [async_http_test() for _ in range(10)]
    results = loop1.run_until_complete(asyncio.gather(*tasks))
    print(time.time() - start)

    # loop 
    for url in urls_todo:
        crawler = Crawler(url)
        crawler.fetch()
    loop()
