# aserver.py
# Fibonacci microservice w/o threading. Supports multiple clients without threading module


from socket import *
from fib import fib
from collections import deque
from select import select
from concurrent.futures import ProcessPoolExecutor as Pool

pool = Pool(4)
tasks = deque()  # make a task queue
recv_wait = { }  # mappings sockets -> tasks (generators)
send_wait = { }
future_wait = { }
future_notify, future_event = socketpair()


def future_done(future):
    tasks.append(future_wait.pop(future))
    future_notify.send(b'x')


def future_monitor():
    while True:
        yield 'recv', future_event
        future_event.recv(100)


tasks.append(future_monitor())


def run():
    while any([tasks, recv_wait, send_wait]):
        while not tasks:
            # No Active tasks to run
            # wait for I/O
            can_recv, can_send, [] = select(recv_wait, send_wait, [])
            for s in can_recv:
                tasks.append(recv_wait.pop(s))
            for s in can_send:
                tasks.append(send_wait.pop(s))                
        task = tasks.popleft()
        try:
            why, what = next(task)  # run to the yield statement
            if why == 'recv':
                # must wait somewhere
                recv_wait[what] = task
            elif why == 'send':
                send_wait[what] = task
            elif why == 'future':
                future_wait[what] = task
                what.add_done_callback(future_done)
            else:
                raise RuntimeError("ARG!")
        except StopIteration:
            print("Task done!")


def fib_server(address):
    sock = socket(AF_INET, SOCK_STREAM)  # create the socket object
    sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)  # create the network port
    sock.bind(address)  # bind the socket to an address
    sock.listen(5)  # tell the system to listen on the port
    while True:
        yield 'recv', sock
        client, addr = sock.accept()  # accept connections on the socket #! BLOCKING
        print ("Connection", addr)
        tasks.append(fib_handler(client))


def fib_handler(client):
    while True:
        yield 'recv', client
        req = client.recv(100)  # receive a request #! BLOCKING
        if not req:
            break
        n = int(req)
        future = pool.submit(fib, n)
        yield 'future', future
        result = future.result()
        resp = str(result).encode('ascii') + b'\n'
        yield 'send', client
        client.send(resp)  #! BLOCKING
    print("Closed")


tasks.append(fib_server(('', 25000)))  # run a fibonacci server at port 25000
run()
