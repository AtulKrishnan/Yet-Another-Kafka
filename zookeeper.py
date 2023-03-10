# import socket programming library
import socket

import os
from time import time, ctime, sleep
import datetime

# import thread module
from _thread import *
import threading

print_lock = threading.Lock()

silent = []
clients = {}


# thread function
def threaded(c, addr):
    while True:

        # data received from client
        data = c.recv(1024)
        if not data:
            print('Bye')
            print("Broker at:", addr, "is Dead")

            # lock released on exit
            print_lock.release()
            break

        modifiedMessage = data.decode('ascii')
        if (modifiedMessage == 'first'):
            modifiedMessage = 'Leader'

        t = ctime(time())
        print(modifiedMessage, addr, t)

        # send back reversed string to client
        c.send(modifiedMessage.encode('ascii'))

    # connection closed
    c.close()


def Main():
    host = ""

    # reserve a port on your computer
    # in our case it is 12345 but it
    # can be anything
    port = 12345
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    print("socket binded to port", port)

    # put the socket into listening mode
    s.listen(5)
    print("socket is listening")

    # a forever loop until client wants to exit
    while True:
        # establish connection with client
        c, addr = s.accept()

        # lock acquired by client
        print_lock.acquire()
        print('Connected to :', addr[0], ':', addr[1])

        # Start a new thread and return its identifier
        start_new_thread(threaded, (c, addr,))
    s.close()


if __name__ == '__main__':
    Main()

