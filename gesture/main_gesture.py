#!/usr/bin/env python3

import socket
import sys
import ev3_hand_detection as gesture

# HOST INFO
HOST = '192.168.0.144'
PORT = 5000


# Debug Print
def debug_print(*args, **kwargs):
    print(*args, **kwargs, file=sys.stderr)


def create_client_socket():
    client_socket = socket.socket()
    client_socket.connect((HOST, PORT))
    debug_print('CLIENT CONNECTED TO SERVER!')

    return client_socket


def main():
    client_socket = create_client_socket()
    data = gesture.capture()

    while True:
        client_socket.send(str(data).encode())


if __name__ == "__main__":
    main()
