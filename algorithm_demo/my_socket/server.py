#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author: Link 
@module: TCPServer 
@date: 2020-06-13 
"""
import socket
from socket import AF_INET, SOCK_STREAM
from typing import NewType, Union
from handler import WriteHandler

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

    def recv(self, client_fd: Socket) -> str:
        """接收数据"""
        data = client_fd.recv(BUFFER_SIZE)
        return data.decode('utf8')

    def send(self, client_fd: Socket, data: Union[str, bytes]) -> None:
        """发送数据"""
        if isinstance(data, str):
            data = data.encode('utf8')
        client_fd.send(data)

    def close(self) -> None:
        """关闭"""
        for fd in self.clients:
            fd.close()

        if self.server_fd:
            self.server_fd.close()


if __name__ == '__main__':
    writer_handler = WriteHandler()
    server = TcpServer1(IP, PORT)

    sfd = server.create_server()
    cfd = server.accept()

    while True:
        msg = server.recv(cfd)
        if msg in ('q', 'Q'):
            break

        print(f'Recv:{msg}, from {server.clients[cfd]}')
        server.send(cfd, writer_handler(msg))

    server.close()

