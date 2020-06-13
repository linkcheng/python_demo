#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author: Link 
@module: TcpClient 
@date: 2020-06-13 
"""
import socket
from socket import AF_INET, SOCK_STREAM

IP = '0.0.0.0'
PORT = 5000
BUFFER_SIZE = 4096
CLIENT_SIZE = 5


class TcpClient1:
    def __init__(self, ip: str, port: int):
        self.ip = ip
        self.port = port
        self.client_fd = None

    def connect(self):
        if not self.client_fd:
            self.client_fd = socket.socket(AF_INET, SOCK_STREAM)
            self.client_fd.connect((self.ip, self.port))
        return self.client_fd

    def close(self):
        if self.client_fd:
            self.client_fd.close()

    def send(self, data):
        if isinstance(data, str):
            data = data.encode('utf8')
        self.client_fd.send(data)

    def recv(self):
        data = self.client_fd.recv(BUFFER_SIZE)
        return data.decode('utf8')


if __name__ == '__main__':
    client = TcpClient1(IP, PORT)
    cfd = client.connect()

    while True:
        data_str = input('>')
        if not data_str:
            break
        client.send(data_str)
        if data_str in ('q', 'Q'):
            break
        msg = client.recv()
        print(f'Recv>{msg}')

    client.close()
