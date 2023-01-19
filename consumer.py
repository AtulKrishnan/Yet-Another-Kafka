# Import socket module
import socket
import datetime
import time
from time import sleep


def Main():
    # local host IP '127.0.0.1'
    host = '127.0.0.2'

    # Define the port on which you want to connect
    port = 12341

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # connect to server on local computer
    s.connect((host, port))

    i = 0
    while True:

        try:

            # message you send to server
            if (i == 0):
                print("Welcome to consumer")
                topic = input("Enter the topic you want to subscribe to: ")
                topic1 = ["c", topic, "0"]
                topic = "c " + topic
                flag = input("Enter --beginning to read from beginning: ")
                if (flag == "--beginning"):
                    topic = topic + ' e'
                    s.send(topic.encode('ascii'))
                else:
                    # currrnt time
                    ct = datetime.datetime.now()
                    # timestamp
                    ts = ct.timestamp()
                    topic = topic + " " + str(ts)
                    s.send(topic.encode('ascii'))
                i = i + 1
            else:
                # currrnt time
                ct = datetime.datetime.now()
                # timestamp
                ts = ct.timestamp()
                time.sleep(20)
                topic1[2] = str(ts)
                topic2 = ' '.join(map(str, topic1))
                s.send(topic2.encode('ascii'))
            # message received from server
            data = s.recv(1024)

            # print the received message
            # here it would be a reverse of sent message
            print('Received from the server :', str(data.decode('ascii')))
        except socket.error:
            connected=False
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            print( "connection lost... reconnecting" )
            while not connected:
                try:
                    s.connect((host, port))
                    connected=True
                    print("we good now")
                except socket.error:
                    sleep(2)

    # ask the client whether he wants to continue
    # ans = input('\nDo you want to continue(y/n) :')
    # if ans == 'y':
    #	continue
    # else:
    #	break
    # close the connection
    s.close()


if __name__ == '__main__':
    Main()
