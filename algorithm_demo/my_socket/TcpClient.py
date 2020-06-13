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

client_fd = socket.socket(AF_INET, SOCK_STREAM)
client_fd.connect((IP, PORT))

client_fd.send('hello'.encode('utf8'))
rcv_byte_data = client_fd.recv(BUFFER_SIZE)
print(f'recv data from server={rcv_byte_data.decode("utf8")}')

client_fd.close()

