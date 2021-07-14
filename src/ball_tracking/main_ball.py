#!/usr/bin/env python3

import socket
import sys
import traceback

import cv2

from green_ball_tracking import track, Exit

# HOST INFO
HOST = '192.168.1.2'
PORT = 50000


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

    try:
        while True:
            # receive instructions from green ball tracker
            data = track()
            # send it to the server
            # sharp (#) char signals beginning of new command
            client_socket.sendall(bytes("#{}".format(data).encode('utf8')))
    except Exit as e:
        print(">> Exit <<", e)
        Exit.quit()
    except Exception as e:
        # for debugging purposes
        print(e)
        tb = traceback.format_exc()
        print(tb)
    finally:
        cv2.destroyAllWindows()
        client_socket.close()
        sys.exit(0)


if __name__ == "__main__":
    main()
