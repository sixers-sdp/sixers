import socket
import ev3dev.ev3 as ev3
import threading
import time
import select

from . import constants

us = ev3.UltrasonicSensor()
us.mode = 'US-DIST-CM'
units = us.units

data = {"server-end": False, "obstacle-found": False, "said": False, "last-command": None, "time-said": time.time()}
BRAKING_TYPE = 'brake'
MOVING_CORNER = False


def move_left(m, m1, value=250):
    m.run_forever(speed_sp=value)
    m1.run_forever(speed_sp=value)


def move_right(m2, m3, value=250):
    m2.run_forever(speed_sp=value)
    m3.run_forever(speed_sp=value)


def go_forward(m, m1, m2, m3, value):
    global motors
    move_left(m, m1, value)
    move_right(m2, m3, value)
    # while(motors["running"]):
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


def move_albert(move, m, m1, m2, m3):
    if (move == constants.MoveCommand.FORWARD.value):
        # motors["running"]=True
        go_forward(m, m1, m2, m3, 200)
    elif move == constants.MoveCommand.ALIGN_LEFT.value:
        # print(response, "ALIGN LEFT")
        align(m, m1, m2, m3, 100, 250)
    elif move == constants.MoveCommand.ALIGN_RIGHT.value:
        # print(response, "ALIGN RIGHT")
        align(m, m1, m2, m3, 250, 100)
    elif (move == constants.MoveCommand.STOP.value):
        # print(response, "STOP")
        stop(m, m1, m2, m3)
    elif (move == constants.MoveCommand.QR.value):
        # print(response, "QR")
        stop(m, m1, m2, m3)
    else:
        corner_type(m, m1, m2, m3, move)


def corner_type(m, m1, m2, m3, c_type):
    if c_type == constants.MoveCommand.CORNER_RIGHT.value:
        move_left(m, m1, 100)
        move_right(m2, m3, -100)
    elif c_type == constants.MoveCommand.CORNER_LEFT.value:
        move_left(m, m1, -100)
        move_right(m2, m3, 100)


def check_for_obstacle(m, m1, m2, m3):
    global data
    while not data["server-end"]:
        distance = us.value() / 10
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
            if data["last-command"] is not None:
                print(data["last-command"])
                move_albert(data["last-command"], m, m1, m2, m3)
                data["last-command"] = None
                data["obstacle-found"] = False

        time.sleep(0.05)


def start_socket(m, m1, m2, m3):
    global data
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((constants.RPI_ADDRESS, constants.PORT))
    while not data['server-end']:
        try:
            ready_to_read, ready_to_write, in_error = select.select([sock, ], [sock, ], [], 5)
        except select.error:
            sock.shutdown(2)  # 0 = done receiving, 1 = done sending, 2 = both
            sock.close()
            # connection error event here, maybe reconnect
            print('connection error')
            data['server-end'] = True
            stop(m, m1, m2, m3)
            break

        if len(ready_to_read) > 0:
            data_type = sock.recv(1).decode()
            if len(data_type) != 1:
                continue
            move = int(data_type)
            print(move)
            data["last-command"] = move
            if data["obstacle-found"]:
                continue
            move_albert(move, m, m1, m2, m3)
    sock.close()


if __name__ == "__main__":
    try:
        m = ev3.LargeMotor('outA')
        m1 = ev3.LargeMotor('outB')
        m2 = ev3.LargeMotor('outC')
        m3 = ev3.LargeMotor('outD')
        if not m.connected:
            print("Plug a motor into port A")
        elif not m1.connected:
            print("Plug a motor into port B")
        elif not m2.connected:
            print("Plug a motor into port C")
        elif not m3.connected:
            print("Plug a motor into port D")
        else:
            obstacle_thread = threading.Thread(target=check_for_obstacle, args=(m, m1, m2, m3,))
            obstacle_thread.daemon = True
            obstacle_thread.start()
            start_socket(m, m1, m2, m3)
    except Exception as e:
        data["server-end"] = True
        print(e)
