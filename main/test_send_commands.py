import os
import sys
import time

sys.path.append(os.path.abspath('..'))
from vision.server import Server

START = 0

commands = [['FORWARD', 'LEFT', 'FORWARD', 'END'],
['FORWARD', 'FORWARD', 'END'],
['FORWARD', 'LEFT', 'LEFT', 'RIGHT', 'END']]

qr_codes = [['c4', 'c2', 'c1', 't1'],
['c1', 'c2', 't2'],
['c2', 'c1', 'c3', 'c4', 'k1']]

colors = [True, False, False]

server = Server()

try:
    for i in range(START, 3):
        server.setup_order(commands[i], colors[i], qr_codes[i])
        time.sleep(2)
        print("woah")
except Exception as e:
    print(e)
    server.crash()
