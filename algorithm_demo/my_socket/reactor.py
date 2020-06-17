#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author: Link 
@module: reactor 
@date: 2020-06-16 
"""
import struct
import socket
from threading import Thread
from socket import AF_INET, SOCK_STREAM
from selectors import DefaultSelector, SelectorKey, EVENT_READ, EVENT_WRITE
from concurrent.futures import ProcessPoolExecutor
from multiprocessing import Queue, Process
from typing import NewType

Socket = NewType('Socket', socket)


class SelectorMixin:
    selector = DefaultSelector()

    def select(self):
        return self.selector.select()

    def register(self, fd: Socket, events: SelectorKey, data=None):
        fd.setblocking(False)
        self.selector.register(fd, events, data)

    def modify(self, fd: Socket, events: SelectorKey, data=None):
        self.selector.modify(fd, events, data)

    def unregister(self, fd):
        self.selector.unregister(fd)

    def close(self):
        self.selector.close()


class Loop(SelectorMixin):
    def __init__(self, server_fd):
        self.server_fd = server_fd
        self.selector = DefaultSelector()

        self.processor_capacity = 8
        self.pq = Queue()
        self.processors = [
            Processor(self.pq) for _ in range(self.processor_capacity)
        ]

        self.acceptor_capacity = 3
        self.acceptors = [
            Acceptor(self.pq) for _ in range(self.acceptor_capacity)
        ]

    def run(self):
        for acceptor in self.acceptors:
            acceptor.start()

        while True:
            events = self.select()
            for key, mask in events:
                if mask == EVENT_READ and key.fileobj == self.server_fd:
                    self.accept()

    def accept(self):
        client_fd, addr = self.server_fd.accept()
        index = client_fd.fileno() % self.acceptor_capacity
        self.acceptors[index].register(client_fd, EVENT_READ)


class Acceptor(Thread, SelectorMixin):
    def __init__(self, pq: Queue):
        super().__init__()
        self.selector = DefaultSelector()
        self.pq = pq

        self.buffer_size = 4096
        self.header_size = struct.calcsize('!I')
        self.data_buffer = {}

    def run(self):
        while True:
            events = self.select()
            for key, mask in events:
                if mask == EVENT_READ:
                    self.read(key.fileobj)
                elif mask == EVENT_WRITE:
                    self.write(key.fileobj, key.data)

    def read(self, client_fd):
        for req in self._read(client_fd):
            data = (self.selector, client_fd, req)
            self.pq.put(data)

    def _read(self, client_fd: Socket):
        """接收数据"""
        data = client_fd.recv(self.buffer_size)
        data_buffer = self.data_buffer.setdefault(client_fd, bytes())
        data_buffer += data

        while len(data_buffer) >= self.header_size:
            # 取包头
            head_pack = struct.unpack('!I', data_buffer[:self.header_size])
            body_size = head_pack[0]

            # 处理分包
            if len(data_buffer) < self.header_size + body_size:
                break

            body = data_buffer[self.header_size: self.header_size+body_size]
            yield body.decode('utf8')

            # 处理粘包
            data_buffer = data_buffer[self.header_size+body_size:]

        self.data_buffer[client_fd] = data_buffer

    def write(self, client_fd, data):
        if isinstance(data, str):
            data = data.encode('utf8')
        if data:
            client_fd.send(data)
        self.modify(client_fd, EVENT_READ)


class Processor(Process):
    def __init__(self, pq: Queue):
        super().__init__()
        self.pq = pq

    def run(self):
        while True:
            selector, client_fd, req = self.pq.get()

            if req and req not in ('q', 'Q'):
                resp = handle(req)
                selector.modify(client_fd, EVENT_WRITE, resp)
            else:
                selector.unregister(client_fd)
                client_fd.close()


def handle(msg):
    return msg.replace("吗", "").replace("?", "!").replace("？", "!")
