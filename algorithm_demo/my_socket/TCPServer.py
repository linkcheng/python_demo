#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author: Link 
@module: TCPServer 
@date: 2020-06-13 
"""
import socket
from socket import AF_INET, SOCK_STREAM

IP = '0.0.0.0'
PORT = 5000
BUFFER_SIZE = 4096
CLIENT_SIZE = 5

server_fd = socket.socket(AF_INET, SOCK_STREAM)
server_fd.bind((IP, PORT))
server_fd.listen(CLIENT_SIZE)

client_fd, addr = server_fd.accept()
rcv_byte_data = client_fd.recv(BUFFER_SIZE)
print(f'recv from {addr}, data={rcv_byte_data.decode("utf8")}')

client_fd.send('hello client'.encode('utf8'))

client_fd.close()
server_fd.close()

