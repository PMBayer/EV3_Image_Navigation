#!/usr/bin/env python3

import socket
import sys
import cv2

import ev3_hand_detection as gesture

# HOST INFO and establishing of client socket
HOST = '192.168.0.116'
PORT = 5001
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


# Debug Print
def debug_print(*args, **kwargs):
    print(*args, **kwargs, file=sys.stderr)


# sends the encoded commands to the server
def send(cmd):
    client_socket.sendall(bytes(cmd.encode('utf8')))


def main():
    # Setting up the camera
    cap = cv2.VideoCapture(0)
    debug_print('VIDEO CAPTURE SET UP!')
    # Connecting to the Server
    client_socket.connect((HOST, PORT))
    debug_print('CLIENT CONNECTED TO SERVER!')

    # if branch: The data is sent for an indefinite period of time until it recieves the closing signal;
    # else branch:for cleaning up purposes; Cleanly shutting down the client and closing active windows opened by the
    # programm; Sending closing signal to server
    while True:
        data = gesture.capture(cap)
        if data != 'end':
            send(data)
            debug_print(data)
            # data = client_socket.recv(1024)
        else:
            cv2.destroyAllWindows()
            send(data)
            debug_print(data)
            client_socket.close()
            break


if __name__ == "__main__":
    main()
