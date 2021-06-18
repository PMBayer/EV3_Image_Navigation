#!/usr/bin/env python3

import socket
import sys
import ev3_hand_detection as gesture

# HOST INFO
HOST = '192.168.0.116'
PORT = 5000
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)



# Debug Print
def debug_print(*args, **kwargs):
    print(*args, **kwargs, file=sys.stderr)


    return client_socket


def send(cmd):
    client_socket.sendall(bytes(cmd.encode('utf8')))


def main():
    client_socket.connect((HOST, PORT))
    debug_print('CLIENT CONNECTED TO SERVER!')

    while True:
        # data = client_socket.recv(1024)
        data = gesture.capture()
        send(data)
        # client_socket.send(data.encode('utf8'))
        # client_socket.send(str(data).encode('utf8'))
        data = client_socket.recv(1024)


if __name__ == "__main__":
    main()
