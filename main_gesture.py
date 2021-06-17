#!/usr/bin/env python3

import socket
import sys

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


if __name__ == "__main__":
    main()
