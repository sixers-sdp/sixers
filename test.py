from time import sleep

import zbar
from cv2.cv2 import imread
from scipy.misc import imread as read_image
from zbar.misc import rgb2gray
import cv2

from pyzbar.pyzbar import decode



im = imread("/home/visgean/qr.jpg")

if len(im.shape) == 3:
    im = rgb2gray(im)
# scan the image for barcodes
scanner = zbar.Scanner()
results = scanner.scan(im)

print(results)
# topLeftCorners, bottomLeftCorners, bottomRightCorners, topRightCorners = [item for item in results.location]


print(decode(im))


vc = cv2.VideoCapture(0)
if not vc.isOpened():
    print("Camera did not open! Trying again in 3 2 1...")
    vc.release()
else:
    print("Camera ready")
    vc.set(3, 160)
    vc.set(4, 120)
    while True:
        frame = vc.read()[1]
        decoded_frame = decode(frame)
        # cv2.imshow("wha", frame)
        # cv2.waitKey(0)
        sleep(0.2)
        if decoded_frame:
            print(decoded_frame)






















