#!/usr/bin/env python
 
"""
A simple echo client (UDP)
"""
 
import socket
 
# configure the client
port = 5000
host = '172.16.206.169'
size = 8192
timeout = 8
testMsg = "This is my //77text123"
 
# initialize socket
try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(timeout)
    sock.sendto(testMsg, (host, port))
    response = sock.recv(8192)
    sock.close()
    if response == testMsg:
        print "connection is working fine."
    else:
        print "connection error occured."
except:
    print "cannot reach your server"