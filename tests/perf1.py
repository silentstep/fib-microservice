# perf1.py
# Measure the time of a long running request

from socket import *
import time


sock = socket(AF_INET, SOCK_STREAM)  # create a socket connection to the server
sock.connect(('localhost', 25000))

while True:  # start the infinite request loop
    start = time.time()  # measure start time
    sock.send(b'30')  # send a request for moderately sized fibonacci number
    resp = sock.recv(100)
    end = time.time()
    print(end-start)
    
