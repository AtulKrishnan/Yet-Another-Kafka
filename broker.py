# import socket programming library
from socket import *
import os
import json
import datetime
import sys
from time import time, ctime, sleep

# from queue import Queue
# import thread module
from _thread import *
import threading
import logging

print_lock = threading.Lock()
num = 1
#log={}



# diction={}
def doesFileExists(filePathAndName):
    return os.path.exists(filePathAndName)


# thread function
def threaded(c,addr):
    while True:

        # data received from client
        data = c.recv(1024)
        if not data:
            print('Bye')

            # lock released on exit
            # print_lock.release()
            break

        # global diction
        message = []

        # Decoding the message
        msg = str(data.decode('ascii'))

        # Splitting into a list
        L = msg.split()

        # producer side
        if (L[0] == 'p'):

            #logging.warning("A WARNING")
            #logging.basicConfig(filename='msg.log', filemode='w', format='%(asctime)s  - %(message)s')
            #logging.info("role :producer")
            #log={'role':'producer','topic':L[1]}
            curr_dir = os.getcwd()
            topic = os.path.join(curr_dir, 'topic.json')
            print(topic)

            if doesFileExists(topic):
                with open(topic) as json_file:
                    files = json.load(json_file)
                json_file.close()
                if L[1] not in files:
                    files[L[1]] = 0
                else:
                    files[L[1]] = files[L[1]] + 1

                with open(topic, 'w') as json_file:
                    json.dump(files, json_file)
                json_file.close()
            else:
                jfile = open(topic, "w")
                jfile.close()

                files = {}
                files[L[1]] = 0

                with open(topic, 'w') as json_file:
                    json.dump(files, json_file)
                json_file.close()

            # currrnt time
            ct = datetime.datetime.now()

            # timestamp
            ts = ct.timestamp()

            # creating directory
            curr_dir = os.getcwd()
            final_dir = os.path.join(curr_dir, L[1])
            if not os.path.exists(final_dir):
                os.makedirs(final_dir)
            print(final_dir)

            # if L[1] not in diction:
            # diction[L[1]]=0

            message = ' '.join(map(str, L[2:]))
            #log.update({'message':message})
            # obj[str(ts)]=message

            filename = str(files[L[1]] // 5 + 1) + '.json'

            print(filename)
            final_dir = os.path.join(curr_dir, L[1] + '/' + filename)
            json_decoded = {}
            if doesFileExists(final_dir):
                with open(final_dir) as json_file:
                    json_decoded = json.load(json_file)
                json_file.close()

                json_decoded[str(ts)] = message

                with open(final_dir, 'w') as json_file:
                    json.dump(json_decoded, json_file)
                json_file.close()
            else:
                jfile = open(final_dir, "w")
                jfile.close()

                json_decoded = {}
                json_decoded[str(ts)] = message

                with open(final_dir, 'w') as json_file:
                    json.dump(json_decoded, json_file)
                json_file.close()
            logging.basicConfig(level=logging.INFO, filename="py_log.log", filemode="a",
                                format="%(asctime)s %(levelname)s %(message)s")
            #logging.debug("A DEBUG Message")
            logging.info(f"\nRole: Producer\nTopic:{L[1]}\nMessage:{message}\nAddress:{addr}\n\n")
            c.send(data)



        if (L[0] == 'c'):
            logging.basicConfig(level=logging.INFO, filename="py_log.log", filemode="a",
                                format="%(asctime)s %(levelname)s %(message)s")
            #logging.debug("A DEBUG Message")
            logging.info(f"\nRole: Consumer\nTopic:{L[1]}\nAddress:{addr}\n\n")
            if (L[-1] == "e"):
                try:

                    out = ""
                    j = 1
                    filename = "1.json"
                    curr_dir = os.getcwd()
                    final_dir = os.path.join(curr_dir, L[1] + '/' + filename)
                    json_decoded = {}
                    message = []

                    while doesFileExists(final_dir):
                        with open(final_dir) as json_file:
                            json_decoded = json.load(json_file)
                        json_file.close()
                        for i in json_decoded:
                            message.append(json_decoded[i]+'\n')
                        j = j + 1
                        filename = str(j) + '.json'
                        final_dir = os.path.join(curr_dir, L[1] + '/' + filename)

                    print(json_decoded)

                    message = ' '.join(map(str, message))

                    c.send(message.encode('ascii'))

                    # f=open(L[1],"r")
                    # print(L[1],f)
                    # lines = f.readlines()
                    # print(lines)
                    # out=out+lines
                    # print(out)
                    # out= ' '.join(map(str, lines))
                    # print(out)
                    # f.close()

                except:
                    out = "No Topic"
                    c.send(out.encode('ascii'))

            try:
                filename = "1.json"
                curr_dir = os.getcwd()
                final_dir = os.path.join(curr_dir, L[1] + '/' + filename)
                j = 1
                message = []
                # print(L)
                json_decoded = {}
                while doesFileExists(final_dir):
                    with open(final_dir) as json_file:
                        json_decoded = json.load(json_file)
                    json_file.close()
                    for i in json_decoded:
                        if (i > L[-1]):
                            message.append(json_decoded[i]+'\n')
                    j = j + 1
                    filename = str(j) + '.json'
                    final_dir = os.path.join(curr_dir, L[1] + '/' + filename)

                if (len(message) == 0):
                    message.append("No updates in the subscibed topic")
                message = ' '.join(map(str, message))
                c.send(message.encode('ascii'))
            except:
                out = "No Topic"
                c.send(out.encode('ascii'))

            # c.send(data.encode('ascii'))

            # send back reversed string to client

    # connection closed
    c.close()


def heartbeat():
    serverName = '127.0.0.1'
    serverPort = 12345
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((serverName, serverPort))
    message = 'first'
    modi = 'first'
    while (1):
        # clientSocket.sendto(message.encode(), (serverName, serverPort))
        # print("Modified", modi)
        if (modi == 'Leader'):
            start_new_thread(server, ())
            message = "Leader1"
        clientSocket.send(message.encode('ascii'))
        modifiedMessage = clientSocket.recv(1024)
        # print(modifiedMessage.decode('ascii'))
        modi = str(modifiedMessage.decode('ascii'))
        sleep(10)
    clientSocket.close()


def server():
    host = ""

    # reserve a port on your computer
    # in our case it is 12345 but it
    # can be anything
    # print_lock.acquire()

    port = 12341
    s = socket(AF_INET, SOCK_STREAM)
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
        # print_lock.acquire()
        print('Connected to :', addr[0], ':', addr[1])

        # Start a new thread and return its identifier
        start_new_thread(threaded, (c,addr,))

        # start_new_thread(broker,())
    s.close()


def Main():
    start_new_thread(heartbeat, ())
    while True:
        print("Alive")
        sleep(10)


if __name__ == '__main__':
    # print("1")
    Main()
