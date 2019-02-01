import cv2
import numpy as np
import time
from server import Server
from threading import Thread
import json

SENDING_VALUE = {"type":"stop","time":"00","direction":"right"}
def connect_to_server_and_loop():
    try:
        host = '192.168.105.135'
        # host = 'LOCALHOST'
        port = 5005

        server = Server(host,port)
        while True:
            server.accept()
            server.send(SENDING_VALUE)
            time.sleep(.1)
    except(KeyboardInterrupt):
        server.close()

def connect_to_vision():
    NUM_GRIDS = 5
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

    left_power = 0
    right_power = 0

    good_angle = 15
    good_angle_error = 3
    none_found = False

    angle_error = 15

    to_turn = 0
    c = 100

    cv2.namedWindow("preview")
    vc = cv2.VideoCapture(0)

    if vc.isOpened(): # try to get the first frame
        rval, frame = vc.read()
    else:
        rval = False

    while rval:
        cv2.imshow("preview", frame)
        rval, frame = vc.read()
        #cv2.imshow("preview", frame)
        key = cv2.waitKey(20)
        if key == 27: # exit on ESC
            break

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        PINK_MIN = np.array([160, 50, 50],np.uint8)
        PINK_MAX = np.array([180, 255, 255],np.uint8)

        frame_threshed = cv2.inRange(hsv, PINK_MIN, PINK_MAX)

        frame = frame_threshed

        CONST = len(frame)//NUM_GRIDS

        grid = np.zeros((NUM_GRIDS,h/NUM_GRIDS,w))
        for i in range(0, NUM_GRIDS):
            grid[i] = frame[CONST*i:CONST*(i+1)]

        #print(grid.shape)
        for i in range(grid.shape[0]):
            none_found = False
            try:
                top_left = np.argwhere(grid[i,0,:]==255)[0][0]
                cv2.rectangle(frame,(top_left-20,i*grid.shape[1]),(top_left+20,i*grid.shape[1]+20),(255,255,255),3)
            except:
                none_found= True
                pass

            try:
                bottom_left = np.argwhere(grid[i,-1,:]==255)[0][0]
                cv2.rectangle(frame,(bottom_left-20,(i+1)*grid.shape[1]),(bottom_left+20,(i+1)*grid.shape[1]-20),(255,255,255),3)

            except:
                pass

            try:
                top_right = np.argwhere(grid[i,0,:]==255)[-1][0]
                cv2.rectangle(frame,(top_right-20,i*grid.shape[1]),(top_right+20,i*grid.shape[1]+20),(255,255,255),3)
            except:
                none_found= True
                pass

            try:
                bottom_right = np.argwhere(grid[i,-1,:]==255)[-1][0]
                cv2.rectangle(frame,(bottom_right-20,(i+1)*grid.shape[1]-1),(bottom_right+20,(i+1)*grid.shape[1]-20),(255,255,255),3)

            except:
                pass

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

                #print("R:",right_angle)
                print(bottom_left)
                print(bottom_right)
                if (none_found):
                    SENDING_VALUE['type'] = 'stop'
                    print('stop')
                elif (bottom_left>=w/2-c and bottom_right<=w/2+c): #and top_left<=w/2-c and top_right>=w/2+c): #((np.abs(left_angle+right_angle)<good_angle)):
                    SENDING_VALUE['type'] = 'stop'
                    SENDING_VALUE['time'] = 'none'
                    print("forward(stop)")
                else:
                    to_turn = int((left_angle+right_angle)/2)
                    SENDING_VALUE['type'] = 'turn'
                    if (np.sign(to_turn)>0):
                        SENDING_VALUE['direction'] = "right"
                    else:
                        SENDING_VALUE['direction'] = "left"
                    SENDING_VALUE['time'] = np.abs(to_turn)*15
                    print("turn",to_turn)


    cv2.destroyWindow("preview")
    vc.release()


if __name__ == '__main__':
    Thread(target = connect_to_server_and_loop).start()
    Thread(target = connect_to_vision).start()
