# perf2.py
# request/sec of a fast request


from threading import Thread
from socket import *
import time


sock = socket(AF_INET, SOCK_STREAM)  # create a socket connection to the server
sock.connect(('localhost', 25000))

n = 0  # start global counter


def monitor():
    global n
    while True:
        time.sleep(1)
        print(n, 'reqs/sec')
        n = 0


Thread(target=monitor).start()
while True:  # start the infinite request loop
    sock.send(b'1')  # send a request for small fibonacci number
    resp = sock.recv(100)
    n += 1
    
