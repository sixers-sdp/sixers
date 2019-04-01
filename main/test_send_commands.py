import os
import sys

sys.path.append(os.path.abspath('..'))
from vision.server2 import Server


commands = ['FORWARD', 'LEFT', 'FORWARD', 'END']

#commands = ['LEFT', 'LEFT', 'END']
qr_codes = ['c4', 'c2', 'c1', 't1']

server = Server()

try:
    server.setup_order(commands, True, qr_codes)
except Exception as e:
    print(e)
    server.crash()
