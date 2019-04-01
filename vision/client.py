#import socket
import threading
from enum import Enum
import ev3dev.ev3 as ev3
import threading
import time
import socket

try:
    us = ev3.UltrasonicSensor()
    us.mode='US-DIST-CM'
    units = us.units
except:
    import sys
    print("Ultrasonic sensor is not connected")
    sys.exit(1)

PORT = 50000
data = {"server-end": False, "obstacle-found": False, "said": False, "last-command": None, "time-said": time.time()}
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
    QR=1
    STOP=2
    ALIGN_LEFT=3
    ALIGN_RIGHT=4
    FORWARD=5
    CORNER_LEFT=6
    CORNER_RIGHT=7
    FRAME_EMPTY = 8
    END = 9
    BACKWARD = "a"
    BACKWARD_ALIGN_LEFT="b"
    BACKWARD_ALIGN_RIGHT="c"


def move_albert(move, m, m1, m2, m3):
    if(move==Type.FORWARD.value):
        #motors["running"]=True
        go_forward(m, m1, m2, m3, 200)
    elif(move==Type.BACKWARD.value):
        #motors["running"]=True
        go_forward(m, m1, m2, m3, -200)
    elif move == Type.ALIGN_LEFT.value:
        #print(response, "ALIGN LEFT")
        align(m, m1, m2, m3, 100, 250)
    elif move == Type.ALIGN_RIGHT.value:
        #print(response, "ALIGN RIGHT")
        align(m, m1, m2, m3, 250, 100)
    elif move == Type.BACKWARD_ALIGN_LEFT.value:
        #print(response, "BACKWARD ALIGN LEFT")
        align(m, m1, m2, m3, -100, -500)
    elif move == Type.BACKWARD_ALIGN_RIGHT.value:
        #print(response, "BACKWARD ALIGN RIGHT")
        align(m, m1, m2, m3, -500, -100)
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
        move_left(m, m1, 100)
        move_right(m2, m3, -100)
    elif c_type == Type.CORNER_LEFT.value:
        move_left(m, m1, -100)
        move_right(m2, m3, 100)

def check_for_obstacle(m, m1, m2, m3):
    global data
    while not data["server-end"]:
        distance = us.value()/10
        if distance < 20:
            print("whatttt")
            data["obstacle-found"] = True
            stop(m, m1, m2, m3)
            if not data["said"] and time.time() - data["time-said"] > 5:
                try:
                    ev3.Sound.speak("Could you please move out!").wait()
                except:
                    pass
                data["time-said"] = time.time()
                data["said"] = True
        else:
            data["said"] = False
            if data["last-command"] != None:
                print(data["last-command"])
                move_albert(data["last-command"], m, m1, m2, m3)
                data["last-command"]=None
                data["obstacle-found"] = False

        time.sleep(0.05)


def start_socket(m, m1, m2, m3):
     global data
     sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
     socket_is_connected = False
     print("Trying to connect to the server...")
     printed = False
     #old_move = None
     while not data['server-end']:
         if not socket_is_connected:
             try:
                 sock.connect(('192.168.105.135', PORT))
                 socket_is_connected = True
             except Exception as e:
                 #print("---"+str(e)+"---")
                 if str(e) != "[Errno 106] Transport endpoint is already connected":
                     stop(m, m1, m2, m3)
                     # connection error event here, maybe reconnect
                     print('Connection lost! Trying again in 3 2 1...')
                     time.sleep(3)
                     printed = False
                     sock.close()
                     old_move = None
                     sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                     socket_is_connected = False
                     stop(m, m1, m2, m3)
                     continue

         if socket_is_connected:
             if not printed:
                 print("Connected to the server...")
                 printed = True
             try:
                 data_type = sock.recv(1).decode()
             except Exception as e:
                 stop(m, m1, m2, m3)
                 print("---"+str(e)+"---")
                 print('Connection lost! Trying again in 3 2 1...')
                 time.sleep(3)
                 printed = False
                 sock.close()
                 old_move = None
                 sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                 socket_is_connected = False
                 continue

             if len(data_type)!=1:
                 continue
             move = data_type if not data_type.isdigit() else int(data_type)
             #if move == old_move:
             #    continue
             print(move)
             if(move==9):
                 stop(m, m1, m2, m3)
                 print('End of order! Trying new order in 3 2 1...')
                 time.sleep(3)
                 printed = False
                 sock.close()
                 old_move = None
                 sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                 socket_is_connected = False
                 continue
             data["last-command"]=move
             #old_move = move
             if (data["obstacle-found"]): continue
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
            obstacle_thread = threading.Thread(target=check_for_obstacle, args=(m, m1, m2, m3, ))
            obstacle_thread.daemon = True
            obstacle_thread.start()
            start_socket(m, m1, m2, m3)
    except Exception as e:
        data["server-end"] = True
        print(e)
