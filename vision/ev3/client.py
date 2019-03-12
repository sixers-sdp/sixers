import socket
import threading
from enum import Enum
import ev3dev.ev3 as ev3


PORT = 50000
data = {"server-end": False}
BRAKING_TYPE='brake'
MOVING_CORNER = False

def move_left(m, m1, value=250):
    m.run_forever(speed_sp=value)
    m1.run_forever(speed_sp=value)

def move_right(m2, m3, value=250):
    m2.run_forever(speed_sp=value)
    m3.run_forever(speed_sp=value)


def go_forward(m, m1, m2, m3, value):
    global motors
    move_left(m ,m1, value)
    move_right(m2, m3, value)
    #while(motors["running"]):
    #    if(not m.is_running and not m1.is_running and not m2.is_running and not m3.is_running):
    #        motors["running"]=False
    #    time.sleep(0.05)

def stop(m, m1, m2, m3):
    m.stop(stop_action=BRAKING_TYPE)
    m1.stop(stop_action=BRAKING_TYPE)
    m2.stop(stop_action=BRAKING_TYPE)
    m3.stop(stop_action=BRAKING_TYPE)

def align(m, m1, m2, m3, left_value, right_value):
    global motors
    move_left(m, m1, left_value)
    move_right(m2, m3, right_value)


class Type(Enum):
    FORWARD=5
    STOP=2
    ALIGN_LEFT=3
    ALIGN_RIGHT=4
    QR=1
    CORNER_LEFT=6
    CORNER_RIGHT=7


def move_albert(move, m, m1, m2, m3):
    if(move==Type.FORWARD.value):
        #motors["running"]=True
        go_forward(m, m1, m2, m3, 300)
    elif move == Type.ALIGN_LEFT.value:
        #print(response, "ALIGN LEFT")
        align(m, m1, m2, m3, 150, 250)
    elif move == Type.ALIGN_RIGHT.value:
        #print(response, "ALIGN RIGHT")
        align(m, m1, m2, m3, 250, 150)
    elif(move==Type.STOP.value):
        #print(response, "STOP")
        stop(m, m1, m2, m3)
    elif(move==Type.QR.value):
        #print(response, "QR")
        stop(m, m1, m2, m3)
    else:
        corner_type(m, m1, m2, m3, move)

def corner_type(m, m1, m2, m3, c_type):
    if c_type == Type.CORNER_RIGHT.value:
        move_left(m, m1, 75)
        move_right(m2, m3, -75)
    elif c_type == Type.CORNER_LEFT.value:
        move_left(m, m1, -75)
        move_right(m2, m3, 75)

def start_socket(m, m1, m2, m3):
     sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
     sock.connect(('192.168.105.135', PORT))
     while not data['server-end']:
         data_type = sock.recv(1).decode()
         if len(data_type)!=1:
             continue 
         move = int(data_type)
         print(move)
         move_albert(move, m, m1, m2, m3)
     sock.close()


if __name__ == "__main__":
    try:
        m=ev3.LargeMotor('outA')
        m1=ev3.LargeMotor('outB')
        m2=ev3.LargeMotor('outC')
        m3=ev3.LargeMotor('outD')
        if not (m.connected):
            print("Plug a motor into port A")
        elif not (m1.connected):
            print("Plug a motor into port B")
        elif not (m2.connected):
            print("Plug a motor into port C")
        elif not (m3.connected):
            print("Plug a motor into port D")
        else:
            start_socket(m, m1, m2, m3)
    except Exception as e:
        data["server-end"] = True
        print(e)
