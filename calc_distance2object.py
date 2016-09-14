import cv2
from collections import deque
import numpy
import argparse
import imutils
import cv2

cv2.namedWindow("preview")
first_cam = cv2.VideoCapture(1)
second_cam = cv2.VideoCapture(0)

cameras  = [first_cam, second_cam]
focal_distances = [0.8, 0.8] #
first_frames = []
for camera in cameras:
    for _ in xrange(20):
        (grabbed, first_frame) = camera.read()
    first_frames.append(first_frame)

distance_between_cameras = 1 #m

#return x_offset, y_offset
def get_object_position(camera_index):
    camera = cameras[camera_index]
    grabbed, frame = camera.read()
    if not grabbed:
        return (-1, -1)
    frame = imutils.resize(frame, width=500)
    gray1 = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray1, (21, 21), 0)
    frameDelta = cv2.absdiff(first_frames[camera_index], gray)
    thresh = cv2.threshold(frameDelta, 75, 255, cv2.THRESH_BINARY)[1]
    thresh = cv2.dilate(thresh, None, iterations=2)
    (x, y, w, h) = cv2.boundingRect(thresh)
    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
    #cv2.imshow("preview", frame)
    if w and h:
        x_mid = x + w / 2
        y_mid = y + h / 2
        frame_height, frame_width, _ = frame.shape
        x_offset = (float(x_mid) / frame_width) - 0.5
        y_offset = 0.5 - (float(y_mid) / frame_height)
        return (x_offset, y_offset)
    return (-1, -1)

import time
while True:
    time.sleep(0.5)
    obj1, obj2 = get_object_position(0), get_object_position(1)
    if obj1 == (-1, -1) or obj2 == (-1, -1):
        continue

    x0, x1 = obj1[0], obj2[0]
    f0, f1 = focal_distances
    z_distance = float(distance_between_cameras) / (x0 / float(f0 - x1 / float(f1)))
    print z_distance

    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break

# cleanup the camera and close any open windows
camera.release()
cv2.destroyAllWindows()
