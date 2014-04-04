#!/usr/bin/env python
 
"""
A simple echo server (UDP)
"""
 
import socket
 
# define servr properties
host = '127.0.0.1'
port = 5000
size = 8192
 
# configure server socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((host, port))
 
# wait for connections
# terminate with 
try:
    while True:
        data, address = sock.recvfrom(size)
        print "datagram from", address
        sock.sendto(data, address)
finally:
    sock.close()



