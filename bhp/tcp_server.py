#!/usr/bin/env python

import socket
import threading

ip='0.0.0.0'
port=10000

server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

server.bind((ip,port))
server.listen(5)

print "listening on %s:%d" % (ip,port)

def handle_recv(client_socket):
    
    recv=client_socket.recv(1024)
    print "received:%s" % recv

    client_socket.send("ACK")

    client_socket.close()
while True:
    client,addr=server.accept()
    print "Accepted connection from:%s:%d" % (addr[0],addr[1])

    recv_handler=threading.Thread(target=handle_recv,args=(client,))
    recv_handler.start()
