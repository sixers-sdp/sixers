import sys
import threading
import cv2
import numpy as np
import time
import socket
from exceptions import IncorrectNode
from pyzbar.pyzbar import decode

import constants


class Server:
    def __init__(self):
        self.frame = None
        self.server_end = False
        self.socket = None
        self.conn = None
        self.addr = None
        self.ip = '0.0.0.0'
        self.port = 50000
        self.directions = None
        self.end = False
        self.corner_detected = False
        self.corner_detected_once = False
        self.is_current_color_green = True
        self.w = 160
        self.old_type = None
        self.sleep = False
        self.exception_raised = False
        self.decoded_frame = -1
        self.last_correcting_time = 0
        self.out_of_track = False
        self.start_threads()


    def setup_order(self, directions, is_current_color_green, qr_codes_expected=None):
        self.directions = directions
        self.is_current_color_green = is_current_color_green
        self.qr_codes_expected = qr_codes_expected
        self.exception_raised = False
        self.start_order()


    def start_threads(self):
        camera_thread = threading.Thread(target=self.start_camera)
        camera_thread.daemon = True
        camera_thread.start()

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((self.ip, self.port))
        self.listen_for_connections()

    def listen_for_connections(self):
        print("Listening for connections...")
        self.socket.listen(1)
        self.conn, self.addr = self.socket.accept()
        print("Connected from ", self.addr)
        print('Commands', self.directions)


    def crash(self):
        print("Crashing.")
        self.server_end = True
        if self.socket:
            self.socket.close()

        sys.exit(1)


    def start_camera(self):
        self.vc = cv2.VideoCapture(0)
        if not self.vc.isOpened():
            print("Camera did not open! Trying again in 3 2 1...")
            self.vc.release()
            time.sleep(3)
            self.start_camera()
            return
        else:
            print("Camera ready")
        self.vc.set(3, 160)
        self.vc.set(4, 120)

        if self.vc is None:
            self.vc.release()
            self.crash()

        camera_fail_counter = 0
        while not self.server_end:
            frame = self.vc.read()[1]
            self.frame = frame
            if frame is None:
                camera_fail_counter += 1

                if camera_fail_counter > 100000:
                    self.vc.release()
                    self.crash()

            time.sleep(0.05)

        self.vc.release()


    def calculate_frame(self):
        prev_time = time.time()
        frame = self.frame

        if frame is None:
            return constants.MoveCommand.FRAME_EMPTY

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        if self.is_current_color_green:
            THRESHOLD_MIN = np.array([38, 25, 25], np.uint8)
            THRESHOLD_MAX = np.array([80, 255, 255], np.uint8)
        else:
            THRESHOLD_MIN = np.array([95, 25, 25], np.uint8)
            THRESHOLD_MAX = np.array([105, 255, 255], np.uint8)

        frame_threshed = cv2.inRange(hsv, THRESHOLD_MIN, THRESHOLD_MAX)

        kernel = np.ones((5, 5), np.uint8)
        frame_threshed = cv2.erode(frame_threshed, kernel, iterations=1)
        frame_threshed = cv2.dilate(frame_threshed, kernel, iterations=1)

        top_left_index = np.argmax(frame_threshed[0] == 255)

        bottom_left_index = np.argmax(frame_threshed[-1] == 255)

        vert_list = frame_threshed.sum(axis=0)
        vert_idx = np.argmax(vert_list) + 1
        #print(np.abs(self.w // 2 - vert_idx))

        # print(1/(time.time()-prev_time))
        # print(top_left_index, bottom_left_index)

        if self.exception_raised:
            print("Wrong QR Code found...")
            raise IncorrectNode(self.decoded_frame.data)

        if self.sleep:
            time.sleep(1)
            self.sleep = False

        if self.end:
            if top_left_index != 0 and bottom_left_index != 0 and np.abs(self.w // 2 - vert_idx) < 70:
                self.server_end = True
                self.socket.close()
                return constants.MoveCommand.END
            return constants.MoveCommand.CORNER_LEFT

        if self.corner_detected and not self.corner_detected_once and top_left_index != 0 and bottom_left_index != 0:
            if np.abs(self.w // 2 - vert_idx) < 35:
                self.directions.pop(0)
                self.corner_detected = False

        if self.corner_detected and not self.corner_detected_once and self.directions[0] == "FORWARD":
            self.directions.pop(0)
            self.corner_detected = False

        if self.corner_detected and self.corner_detected_once:
            time.sleep(1.25)
            #print("Choosing to turn in the corner...")
            self.corner_detected_once = False
            if self.directions[0] == "LEFT":
                self.is_current_color_green = not self.is_current_color_green
                return constants.MoveCommand.CORNER_LEFT
            elif self.directions[0] == "RIGHT":
                self.is_current_color_green = not self.is_current_color_green
                return constants.MoveCommand.CORNER_RIGHT
            elif self.directions[0] == "FORWARD":
                self.sleep = True
                return constants.MoveCommand.FORWARD
            elif self.directions[0] == "END":
                self.end = True
                return constants.MoveCommand.CORNER_LEFT
            return constants.MoveCommand.STOP

        if not self.corner_detected:
            decoded_frame = decode(frame)
            #print(1 / (time.time() - prev_time))
            if len(decoded_frame) > 0:
                self.decoded_frame = decoded_frame[0]

                node_found = self.decoded_frame.data.lower()
                try:
                    position = self.qr_codes_expected.index(node_found)
                    self.qr_codes_expected = self.qr_codes_expected[position+1:]
                    self.qr_codes_expected.pop(0)
                    self.corner_detected = True
                    self.corner_detected_once = True
                    return constants.MoveCommand.FORWARD
                except ValueError:
                    self.exception_raised = True
                    return constants.MoveCommand.END
            elif top_left_index == 0 and bottom_left_index == 0:
                return constants.MoveCommand.STOP
            if np.abs(self.w // 2 - vert_idx) > 15:
                if self.w // 2 - vert_idx > 0:
                    return constants.MoveCommand.ALIGN_LEFT
                else:
                    return constants.MoveCommand.ALIGN_RIGHT
            else:
                return constants.MoveCommand.FORWARD
        else:
            return self.old_type


    def start_order(self):
        correcting = False
        correcting_command_sent = False
        while not self.server_end:
            new_type = self.calculate_frame()
            if self.old_type != constants.MoveCommand.STOP \
                      and self.old_type != constants.MoveCommand.FRAME_EMPTY \
                         and new_type == constants.MoveCommand.STOP \
                            and self.old_type != None and not correcting:
		self.last_correcting_time = time.time()
                if self.old_type == constants.MoveCommand.ALIGN_RIGHT:
                    print("GO BACKWARD_ALIGN_LEFT")
                    new_type = constants.MoveCommand.BACKWARD_ALIGN_LEFT
                elif self.old_type == constants.MoveCommand.ALIGN_LEFT:
                    print("GO BACKWARD_ALIGN_RIGHT")
                    new_type = constants.MoveCommand.BACKWARD_ALIGN_RIGHT
                elif self.old_type == constants.MoveCommand.FORWARD:
                    print("GO BACKWARD")
                    new_type = constants.MoveCommand.BACKWARD
                correcting = True
            elif new_type != constants.MoveCommand.STOP and correcting:
                #print("Done correcting!")
                correcting_command_sent = False
                correcting = False
            if correcting and correcting_command_sent:
		if (time.time()-self.last_correcting_time > 5) and self.last_correcting_time != -1:
                    self.old_type = constants.MoveCommand.STOP
                    new_type = self.old_type
                    self.last_correcting_time = -1
                else:
                    new_type = self.old_type
                    continue
            if self.old_type == new_type and not correcting:
                continue
            print('New command is', new_type)
            try:
                if isinstance(new_type, int):
                    print('received int type command from calculate_frame, use enum!')
                    self.conn.sendall(str(new_type).encode())
                if new_type is not None:
                    self.conn.sendall(str(new_type.value).encode())
            except Exception as e:
                self.listen_for_connections()
                self.conn.sendall(str(self.calculate_frame().value).encode())
                continue
            if correcting:
                correcting_command_sent = True
            self.old_type = new_type
        self.server_end = False
        self.end = False
        return True

if __name__ == "__main__":
    server = Server()
    try:
        server.run()
    except Exception as e:
        server.crash()
        print(e)

