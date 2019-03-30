import os
import sys

sys.path.append(os.path.abspath('..'))
from vision.server2 import Server


commands = ['LEFT', 'LEFT', 'END']
qr_codes = ['t1', 't2']

server = Server()

try:
    server.setup_order(commands, True, qr_codes)
except Exception as e:
    print(e)
    server.crash()
