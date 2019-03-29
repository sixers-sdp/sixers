import os
import socket
import sys

sys.path.append(os.path.abspath('..'))

from vision.constants import PORT

from vision.server import start_socket

GLOBAL_EV3_SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
GLOBAL_EV3_SOCKET.bind(('0.0.0.0', PORT))
GLOBAL_EV3_SOCKET.listen(1)
GLOBAL_EV3_CONN, GLOBAL_EV3_ADDRESS = GLOBAL_EV3_SOCKET.accept()

commands = ['LEFT', 'LEFT', 'END']

try:
    start_socket(commands, GLOBAL_EV3_SOCKET, GLOBAL_EV3_CONN, GLOBAL_EV3_ADDRESS, True)
except Exception as e:
    GLOBAL_EV3_SOCKET.close()
    raise e