from enum import Enum

RPI_ADDRESS = '192.168.105.135'
PORT = 50000


class MoveCommand(Enum):
    QR = 1
    STOP = 2
    ALIGN_LEFT = 3
    ALIGN_RIGHT = 4
    FORWARD = 5
    CORNER_LEFT = 6
    CORNER_RIGHT = 7
    FRAME_EMPTY = 8
    END = 9
