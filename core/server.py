# server.py
# Fibonacci microservice


from socket import *
from fib import fib
from threading import Thread


def fib_server(address):
    sock = socket(AF_INET, SOCK_STREAM)  # create the socket object
    sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)  # create the network port
    sock.bind(address)  # bind the socket to an address
    sock.listen(5)  # tell the system to listen on the port
    while True:
        client, addr = sock.accept()  # accept connections on the socket
        print ("Connection", addr)
        Thread(target=fib_handler, args=(client,), daemon=True).start()


def fib_handler(client):
    while True:
        req = client.recv(100)  # receive a request
        if not req:
            break
        n = int(req)
        result = fib(n)
        resp = str(result).encode('ascii') + b'\n'
        client.send(resp)
    print("Closed")


fib_server(('', 25000))  # run a fibonacci server at port 25000
