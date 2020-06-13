#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author: Link 
@module: TCPServer 
@date: 2020-06-13 
"""
import socket
import selectors
from socket import AF_INET, SOCK_STREAM
from selectors import DefaultSelector, SelectorKey, EVENT_READ, EVENT_WRITE
from typing import NewType, Union

Socket = NewType('socket', socket)
IP = '0.0.0.0'
PORT = 5000
BUFFER_SIZE = 4096
CLIENT_SIZE = 5


class TcpServer1:
    def __init__(self, ip: str, port: int):
        self.ip = ip
        self.port = port
        self.server_fd = None
        self.clients = {}

    def create_server(self) -> Socket:
        """创建服务端 socket"""
        if not self.server_fd:
            self.server_fd = socket.socket(AF_INET, SOCK_STREAM)
            self.server_fd.bind((self.ip, self.port))
            self.server_fd.listen(CLIENT_SIZE)
        return self.server_fd

    def accept(self) -> Socket:
        """获取客户端 socket"""
        client_fd, addr = self.server_fd.accept()
        self.clients[client_fd] = addr
        return client_fd

    def close(self) -> None:
        """关闭"""
        for fd in self.clients:
            fd.close()

        if self.server_fd:
            self.server_fd.close()


class Handler:
    def __init__(self, server: TcpServer1):
        self.server = server

    def accept(self, sock) -> Socket:
        """获取客户端 socket"""
        if sock != self.server.server_fd:
            return sock

        client_fd, addr = self.server.server_fd.accept()
        print(f'Client {addr} connected')
        self.server.clients[client_fd] = addr
        return client_fd

    def read(self, client_fd: Socket):
        """接收数据"""
        data = client_fd.recv(BUFFER_SIZE)
        return data.decode('utf8')

    def send(self, client_fd: Socket, data: Union[str, bytes]) -> None:
        """发送数据"""
        if isinstance(data, str):
            data = data.encode('utf8')
        if data:
            client_fd.send(data)

    def handle(self, conn, msg):
        print(f'Recv:{msg}, from {self.server.clients[conn]}')
        return msg.replace("吗", "").replace("?", "!").replace("？", "!")

    def close(self, conn):
        conn.close()
        addr = self.server.clients.pop(conn)
        print(f'Client {addr} closed')


class EventLoop:
    def __init__(self, server_id, handler: Handler):
        self.select = DefaultSelector()
        self.server_id = server_id
        self.handler = handler
        self.buffer = {}

    def register(self, fd: Socket, events: SelectorKey, data=None):
        fd.setblocking(False)
        self.select.register(fd, events, data)

    def unregister(self, fd):
        self.select.unregister(fd)

    def run(self):
        loop.register(self.server_id, selectors.EVENT_READ, self.accept)

        while True:
            events = self.select.select()
            for key, mask in events:
                if mask == EVENT_READ:
                    if key.fileobj == self.server_id:
                        self.accept(key.fileobj)
                    else:
                        self.read(key.fileobj)
                elif mask == EVENT_WRITE:
                    self.write(key.fileobj)

    def accept(self, sock):
        """sock 要处理的 fd, mask 为事件类型 READ or WRITE"""
        conn = self.handler.accept(sock)  # Should be ready
        self.register(conn, EVENT_READ | EVENT_WRITE, self.read)

    def read(self, conn):
        data = self.handler.read(conn)
        if data and data not in ('q', 'Q'):
            self.buffer[conn] = self.handler.handle(conn, data)
        else:
            self.unregister(conn)
            self.handler.close(conn)

    def write(self, conn):
        self.handler.send(conn, self.buffer.pop(conn, None))


if __name__ == '__main__':
    svr = TcpServer1(IP, PORT)
    sfd = svr.create_server()
    loop = EventLoop(sfd, Handler(svr))

    print('start server')
    try:
        loop.run()
    finally:
        print('close server')
        svr.close()

