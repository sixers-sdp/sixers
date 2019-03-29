import os
import socket
import sys

sys.path.append(os.path.abspath('..'))

from vision.constants import PORT

from vision.server2 import Server


commands = ['LEFT', 'LEFT', 'END']

server = Server()

try:
    server.setup_order(commands, True)
except Exception as e:
    print(e)
    server.crash()
