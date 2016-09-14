import cv2
from collections import deque
import numpy as np
import argparse
import imutils
import cv2

cv2.namedWindow("preview")
#vc = cv2.VideoCapture(0)
camera = cv2.VideoCapture(0)



# define the lower and upper boundaries of the "green"
# ball in the HSV color space, then initialize the
# list of tracked points
greenLower = (29, 86, 6)
greenUpper = (64, 255, 255)
#pts = deque(maxlen=args["buffer"])

# keep looping
first_frame=None
first = True


for _ in xrange(20):
  (grabbed, frame) = camera.read()
  

while True:
	# grab the current frame
	(grabbed, frame) = camera.read()
 
	# if we are viewing a video and we did not grab a frame,
	# then we have reached the end of the video
	if not grabbed:
		break
	# resize the frame, blur it, and convert it to the HSV
	# color space
	frame = imutils.resize(frame, width=500)
	# blurred = cv2.GaussianBlur(frame, (11, 11), 0)
	gray1 = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	gray = cv2.GaussianBlur(gray1, (21, 21), 0)
	if first:
	  first_frame = gray
          first = False
	  continue
	
	frameDelta = cv2.absdiff(first_frame, gray)
	thresh = cv2.threshold(frameDelta, 75, 255, cv2.THRESH_BINARY)[1]
 
	# dilate the thresholded image to fill in holes, then find contours
	# on thresholded image
	thresh = cv2.dilate(thresh, None, iterations=2)
	#cnts, _, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	#cnts, _, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        (x, y, w, h) = cv2.boundingRect(thresh)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
	cv2.imshow("preview", frame)
        
	#cnts, h = cv2.findContours(thresh.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
 

	# loop over the contours
        """
	for c in cnts:
		# if the contour is too small, ignore it
                if not sum(c):
                  continue
                #if cv2.contourArea(c) < 5:
		#  continue
		# compute the bounding box for the contour, draw it on the frame,
		# and update the text
		(x, y, w, h) = cv2.boundingRect(c)
                if w < 10:
                  continue
                print x, y, w, h
		cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
		text = "Occupied"
        """

	# show the frame to our screen
	#cv2.imshow("preview", frame)
	#cv2.imshow("preview", thresh)

	key = cv2.waitKey(1) & 0xFF

	# if the 'q' key is pressed, stop the loop
	if key == ord("q"):
		break

# cleanup the camera and close any open windows
camera.release()
cv2.destroyAllWindows()
