import cv2
import numpy as np
import time as global_time
from server import Server
from threading import Thread
import json
from motor_board import start_specific_motor, stop_specific_motor, stop_all_motors


class Motor:
    def __init__(self, id):
        self.motor_id=id

    def forward(self, speed=100):
        start_specific_motor(self.motor_id, speed)

    def backward(self, speed=-100):
        if(speed>0): speed=-1*speed
        start_specific_motor(self.motor_id, speed)

    def stop(self):
        stop_specific_motor(self.motor_id)


class AlbertMotion:
    def __init__(self, id_1, id_2):
        self.motor_1 = Motor(id_1)
        self.motor_2 = Motor(id_2)

    def forward(self, speed=80, time=0.25):
        self.motor_1.forward(speed)
        self.motor_2.forward(speed)
        global_time.sleep(time)
        self.stop()

    def backward(self, speed=-80, time=0.35):
        if(speed>0): speed=-1*speed
        self.motor_1.backward(speed)
        self.motor_2.backward(speed)
        global_time.sleep(time)
        self.stop()

    def turn_left(self, speed=80, time=0.5, turn_in_place=False):
        if(turn_in_place):
            self.motor_1.backward(speed)
        self.motor_2.forward(speed)
        global_time.sleep(time)
        self.stop()

    def turn_right(self, speed=80, time=0.5, turn_in_place=False):
        self.motor_1.forward(speed)
        if(turn_in_place):
            self.motor_2.backward(speed)
        global_time.sleep(time)

    def stop(self):
        stop_all_motors()

class Albert:
    def __init__(self):
        self.motion = AlbertMotion(4,2)

camera={"frame": None, "thread": None}

def start_camera(cam):
    global camera
    while True:
        camera["frame"] = cam.read()[1]
        #print("Wait what")


def connect_to_vision(albert):
    global camera
    NUM_GRIDS = 25
    HUE_THRESHOLD = 10
    SATURATION_THRESHOLD = 20
    h=480
    w=640
    HUE = 170
    SATURATION = 80
    RED_THRESHOLD = 200
    top_left = 1
    bottom_left = 0
    top_right = 1
    bottom_right = 0

    FRAME_SLEEP=0.1

    left_power = 0
    right_power = 0

    good_angle = 25
    good_angle_error = 3
    none_found = False

    angle_error = 15

    to_turn = 0
    c = 175

    #cv2.namedWindow("preview")
    vc = cv2.VideoCapture(0)
    camera["thread"] = Thread(target=start_camera, args=(vc, ))
    camera["thread"].daemon = True
    camera["thread"].start()

    #if vc.isOpened(): # try to get the first frame
    #    rval, frame = vc.read()
    #else:
    #    rval = False


    while True:
        prev = global_time.time()
        #cv2.imshow("preview", frame)
        frame = camera["frame"]
        if(frame is None): continue
        key = cv2.waitKey(1)
        if key == 27: # exit on ESC
            break

        #print("Frame Rate: "+str(global_time.time()-prev))

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        PINK_MIN = np.array([160, 50, 50],np.uint8)
        PINK_MAX = np.array([180, 255, 255],np.uint8)

        frame_threshed = cv2.inRange(hsv, PINK_MIN, PINK_MAX)

        frame = frame_threshed

        CONST = len(frame)//NUM_GRIDS

        grid = np.zeros((NUM_GRIDS,h/NUM_GRIDS,w))
        for i in range(0, NUM_GRIDS):
            grid[i] = frame[CONST*i:CONST*(i+1)]

        for i in range(grid.shape[0]-1, grid.shape[0]):
            none_found = False
            try:
                top_left = np.argwhere(grid[i,0,:]==255)[0][0]
                #cv2.rectangle(frame,(top_left-20,i*grid.shape[1]),(top_left+20,i*grid.shape[1]+20),(255,255,255),3)
            except:
                #print("Yolo")
                none_found = True

            try:
                bottom_left = np.argwhere(grid[i,-1,:]==255)[0][0]
                #cv2.rectangle(frame,(bottom_left-20,(i+1)*grid.shape[1]),(bottom_left+20,(i+1)*grid.shape[1]-20),(255,255,255),3)

            except:
                pass

            try:
                top_right = np.argwhere(grid[i,0,:]==255)[-1][0]
                #cv2.rectangle(frame,(top_right-20,i*grid.shape[1]),(top_right+20,i*grid.shape[1]+20),(255,255,255),3)
            except:
                #print("Yolo")
                none_found= True

            try:
                bottom_right = np.argwhere(grid[i,-1,:]==255)[-1][0]
                #cv2.rectangle(frame,(bottom_right-20,(i+1)*grid.shape[1]-1),(bottom_right+20,(i+1)*grid.shape[1]-20),(255,255,255),3)

            except:
                pass

            #global_time.sleep(FRAME_SLEEP)
            #print("Before Conditioning: "+str(global_time.time()-prev))
            #print()

            if (i==grid.shape[0]-1):
                a = top_left-bottom_left
                if (a==0):
                    a=0.00000001

                b = top_right-bottom_right
                if (b==0):
                    b=0.00000001
                left_angle = np.degrees(np.arctan(float(grid.shape[1])/(a)))
                left_angle = np.sign(left_angle)*(90-np.abs(left_angle))

                right_angle = np.degrees(np.arctan(float(grid.shape[1])/(b)))
                right_angle = np.sign(right_angle)*(90-np.abs(right_angle))

                #print("Before Action: "+str(global_time.time()-prev))

                if (none_found):
                    albert.motion.stop()
                    print("Stop")
                #elif ((bottom_left>=((w/2)-c)) and (bottom_right<=((w/2)+c))):
                elif ((np.abs(left_angle+right_angle)<good_angle)):
                    if (bottom_left<((w/2)-c)):
                        print("Forwards (slight right)")
                        albert.motion.turn_left(time =0.1,turn_in_place=True)
                    elif (bottom_right>((w/2)+c)):
                        print("Forwards (slight left)")
                        albert.motion.turn_right(time=0.1,turn_in_place=True)
                    else:
                        print("Forwards")
                        albert.motion.forward(time=0.1)
                else:
                    print("Turn")
                    to_turn = int((left_angle+right_angle)/2)
                    if (np.sign(to_turn)>0):
                        albert.motion.turn_right(time=0.1,turn_in_place=False)
                    else:
                        albert.motion.turn_left(time=0.1,turn_in_place=False)
        #print("Entire loop: "+str(global_time.time()-prev))

    cv2.destroyWindow("preview")
    vc.release()

if __name__ == '__main__':
     try:
        albert = Albert()
        connect_to_vision(albert)
     except(KeyboardInterrupt):
        albert.motion.stop()
