import cv2
import numpy as np
from matplotlib import pyplot as plt

# Get the webcam "0". 
# You can also pass video files as the arguments here and it'll work exactly the same!
video_capture = cv2.VideoCapture(0)

def fn_pass(x):
    pass

cv2.namedWindow('Control')
cv2.createTrackbar('Kernel Size','Control',0,20,fn_pass)

while True:
    # Get the most current frame from video capture
    ret, frame = video_capture.read()

    # Resize the frame for faster processing
    frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)

    # If no return, break
    if not ret:
        break

    # Convert the color frame to greyscale
    frame_bw = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Blur the frame, kernel must be an NxN matrix, where N is odd
    kern_n = (cv2.getTrackbarPos('Kernel Size','Control')//1)*2 + 1
    frame_bw_blur = cv2.GaussianBlur(frame_bw, (kern_n,kern_n), 0)

    # Process the frames in different ways
    frame_laplace = cv2.Laplacian(frame_bw_blur, cv2.CV_64F)
    frame_sobelx = cv2.Sobel(frame_bw_blur, cv2.CV_64F, 1, 0, ksize=5)
    frame_sobely = cv2.Sobel(frame_bw_blur, cv2.CV_64F, 0, 1, ksize=5)

    #cv2.imshow('Input',frame_bw)
    #cv2.imshow('Blur',frame_bw_blur)
    cv2.imshow('Laplace',frame_laplace)
    #cv2.imshow('Sobel X',frame_sobelx)
    #cv2.imshow('Sobel Y',frame_sobely)

    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()
video_capture.release()
