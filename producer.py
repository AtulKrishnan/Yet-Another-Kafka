# Import socket module
import socket


def Main():
    # local host IP '127.0.0.1'
    host = '127.0.0.1'

    # Define the port on which you want to connect
    port = 12341

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # connect to server on local computer
    s.connect((host, port))
    connected=True

    while True:

        # message you send to server
        try:
            print("welcome to producer \n")
            topic = input("Enter the topic you want to publish to: ")
            message1 = input("Enter your message: ")
            message = 'p ' + topic + " " + message1

            # message sent to server
            s.send(message.encode('ascii'))

            # message received from server
            data = s.recv(1024)

            # print the received message
            print('Received from the server :', str(data.decode('ascii')))

            # ask the client whether he wants to continue
            #ans = input('\nDo you want to continue(y/n) :')
            print("adios")
            #if ans == 'y':
            #

            #else:
            break
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

    # close the connection
    s.close()


if __name__ == '__main__':
    Main()