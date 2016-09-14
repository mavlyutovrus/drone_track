import cv2
from collections import deque
import numpy
import argparse
import imutils
import cv2

cv2.namedWindow("preview")
camera = cv2.VideoCapture(1)

first_frame=None
first = True
for _ in xrange(20):
  (grabbed, frame) = camera.read()


focal_distances = []

z_distance2object = 3 #meters
x_distance2object = 0.5 #meters

while True:
    grabbed, frame = camera.read()
    if not grabbed:
        break
    frame = imutils.resize(frame, width=500)
    gray1 = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray1, (21, 21), 0)
    if first:
        first_frame = gray
        first = False
        continue

    frameDelta = cv2.absdiff(first_frame, gray)
    thresh = cv2.threshold(frameDelta, 75, 255, cv2.THRESH_BINARY)[1]
    thresh = cv2.dilate(thresh, None, iterations=2)
    (x, y, w, h) = cv2.boundingRect(thresh)

    if w and h:
        x_mid = x + w/2
        y_mid = y + h/2
        frame_height, frame_width, _= frame.shape
        x_offset = (float(x_mid) / frame_width) - 0.5
        y_offset = 0.5 - (float(y_mid) / frame_height)
        focal_distance = x_offset * float(z_distance2object) / x_distance2object
        focal_distances += [focal_distance]
        print "focal", focal_distance, numpy.median(focal_distances)

    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
    cv2.imshow("preview", frame)
    import time
    #time.sleep(1)
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break

# cleanup the camera and close any open windows
camera.release()
cv2.destroyAllWindows()
