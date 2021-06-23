#!/usr/bin/env python3

import socket
import sys

import cv2

import ev3_hand_detection as gesture

# HOST INFO
HOST = '192.168.0.144'
PORT = 5000
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


# Debug Print
def debug_print(*args, **kwargs):
    print(*args, **kwargs, file=sys.stderr)


def send(cmd):
    client_socket.sendall(bytes(cmd.encode('utf8')))


def main():
    cap = cv2.VideoCapture(0)
    debug_print('VIDEO CAPTURE SET UP!')
    client_socket.connect((HOST, PORT))
    debug_print('CLIENT CONNECTED TO SERVER!')

    while True:
        data = gesture.capture(cap)
        send(data)
        data = client_socket.recv(1024)


if __name__ == "__main__":
    main()
