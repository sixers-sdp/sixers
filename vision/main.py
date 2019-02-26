import cv2
import numpy as np
import time as global_time
from threading import Thread
import json
from motor_board import start_specific_motor, stop_specific_motor, stop_all_motors

def enum(*args):
    enums = dict(zip(args, range(len(args))))
    return type('Enum', (), enums)

Directions = enum('LEFT', 'RIGHT', 'STRAIGHT')

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

    def forward(self, speed=100, time=0.30):
        self.motor_1.forward(speed)
        self.motor_2.forward(speed)
        global_time.sleep(time)
	#self.motor_1.stop()
        #self.stop()

    def backward(self, speed=-100, time=0.30):
        if(speed>0): speed=-1*speed
        self.motor_1.backward(speed)
        self.motor_2.backward(speed)
        global_time.sleep(time)
        #self.stop()

    def turn_left(self, speed=100, time=0.5, turn_in_place=False):
    	if(turn_in_place):
    	    self.motor_1.backward(speed)
    	self.motor_2.forward(speed)
    	global_time.sleep(time)
        #self.stop()

    def turn_right(self, speed=100, time=0.5, turn_in_place=False):
    	self.motor_1.forward(speed)
    	if(turn_in_place):
    	    self.motor_2.backward(speed)
    	global_time.sleep(time)
    	#self.motor_1.forward(speed)
        #self.stop()

    def stop(self):
        stop_all_motors()

class Albert:
    def __init__(self):
	self.motion = AlbertMotion(4,2)

camera={"frame": None, "thread": None, "end": False}

def start_camera(cam):
    global camera
    while not camera["end"]:
        #start_time = global_time.time()
        camera["frame"] = cam.read()[1]
        #print(global_time.time()-start_time)


def connect_to_vision(albert):
    global camera

    NUM_GRIDS = 31


    saw_corner = False
    directions = [1, 1, 0]


    #NUM_GRIDS_i = NUM_GRIDS
    #NUM_GRIDS_j = int(round(NUM_GRIDS*.75))

    NUM_GRIDS_i = 640
    NUM_GRIDS_j =480

    horz_best = int(NUM_GRIDS_i/2)
    vert_best = NUM_GRIDS_j

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

    good_angle = 40
    good_angle_error = 3
    none_found = False

    angle_error = 15

    to_turn = 0
    c = 160
    ALLOW = 10

    #cv2.namedWindow("preview")
    vc = cv2.VideoCapture(0)
    camera["thread"] = Thread(target=start_camera, args=(vc, ))
    camera["thread"].daemon = True
    camera["thread"].start()

    #if vc.isOpened(): # try to get the first frame
    #    rval, frame = vc.read()
    #else:
    #    rval = False

    running_index = 0
    i=0
    while True:
        prev = global_time.time()
        frame = camera["frame"]
        if(frame is None): continue
        key = cv2.waitKey(1)
        if key == 27: # exit on ESC
            break

        #print("Frame Rate: "+str(global_time.time()-prev))

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        PINK_MIN = np.array([0, 50, 50],np.uint8)
        PINK_MAX = np.array([4, 255, 255],np.uint8)

        frame_threshed = cv2.inRange(hsv, PINK_MIN, PINK_MAX)

	kernel = np.ones((5,5),np.uint8)
    	frame_threshed = cv2.dilate(frame_threshed,kernel,iterations=10)

        frame = frame_threshed

        #CONST_i = w//NUM_GRIDS_i
        #CONST_j = h//NUM_GRIDS_j

        #grid = np.zeros((NUM_GRIDS_i,NUM_GRIDS_j,int(h/NUM_GRIDS_j),int(w/NUM_GRIDS_i)))
        #grid = np.zeros((NUM_GRIDS_i,NUM_GRIDS_j))

        #horz_list = np.zeros(NUM_GRIDS_i)
        #vert_list = np.zeros(NUM_GRIDS_j)

        #for i in range(0, NUM_GRIDS_i):
        #    for j in range(0, NUM_GRIDS_j):
        #        grid[i,j] = np.sum(frame[CONST_j*j:CONST_j*(j+1),CONST_i*i:CONST_i*(i+1)])


        #for i in range(NUM_GRIDS_i):
        #    horz_list[i] = np.sum(frame[i,:])

        #for j in range(NUM_GRIDS_j):
        #    vert_list[j] = np.sum(frame[:,j])

        horz_list =  frame.sum(axis=0)
        vert_list = frame.sum(axis=1)

        horz_idx = np.argmax(horz_list)+1
        vert_idx = np.argmax(vert_list)+1

        horz_diff = horz_best-horz_idx
        vert_diff = vert_best-vert_idx

        print(h-vert_idx)
        #saw_corner = True


        if i < 5:
	    i+=1
            continue
        print(global_time.time() - prev)
	#continue
        #if(len(directions) == 0):
        #    print("Order Complete!")
        #    global_time.sleep(1)
        #    continue

        if (not saw_corner and h - vert_idx > 150):
            albert.motion.stop()
            saw_corner = True
            albert.motion.stop()
            global_time.sleep(0.2)
	    albert.motion.forward(time=0.3)
            global_time.sleep(0.2)
            albert.motion.stop()
            global_time.sleep(0.4)
            print("Stop! Corner!")
        elif saw_corner and h - vert_idx <= 150:
            saw_corner = False
            directions = directions[1:]
            print("Corner Escaped")

	if (saw_corner):
            direction = directions[0]
            if direction == Directions.LEFT:
                #albert.motion.forward(time=0.25)
                #albert.motion.stop()
                #global_time.sleep(0.4)
                albert.motion.turn_left(time=0.4, turn_in_place=True)
                global_time.sleep(0.25)
                albert.motion.stop()
                global_time.sleep(0.4)
                print("CORNER LEFT")
            elif direction == Directions.RIGHT:
                #albert.motion.forward(time=0.25)
                #albert.motion.stop()
                #global_time.sleep(0.4)
                albert.motion.turn_right(time=0.4, turn_in_place=True)
                global_time.sleep(0.25)
                albert.motion.stop()
                global_time.sleep(0.4)
                print("CORNER RIGHT")
            else:
                albert.motion.forward(time=0.1)
                global_time.sleep(0.1)
                albert.motion.stop()
                global_time.sleep(0.4)
                print("CORNER STRAIGHT")
            continue
        else:
            if (np.abs(w//2 - horz_idx)>50):
                if (w//2 - horz_idx < 0):
                    print("Slight Right")
                    albert.motion.turn_right(time=0.25,turn_in_place=True)
                else:
                    print("Slight Left")
                    albert.motion.turn_left(time=0.25,turn_in_place=True)
            else:
                albert.motion.forward(time=0.3)
                print("Forwards")

	running_index += 1
        if not saw_corner and running_index > 0:
	    albert.motion.stop()
            print("Stopping to optimise speed")
            global_time.sleep(0.05)
            running_index = 0
        #print(global_time.time()-prev)

    cv2.destroyWindow("preview")
    vc.release()


def main():
     global camera
     try:
        albert = Albert()
        connect_to_vision(albert)
     except(KeyboardInterrupt):
        albert.motion.stop()
        camera["end"]=True

if __name__ == '__main__':
     main()
