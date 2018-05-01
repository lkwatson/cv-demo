import cv2
import numpy as np
import pickle

cap = cv2.VideoCapture(0)

def fn_pass(x):
    pass

cv2.namedWindow('Control')
cv2.createTrackbar('Hue Lower','Control',0,180,fn_pass)
cv2.createTrackbar('Hue Upper','Control',0,180,fn_pass)
cv2.createTrackbar('Sat Lower','Control',0,255,fn_pass)
cv2.createTrackbar('Sat Upper','Control',0,255,fn_pass)
cv2.createTrackbar('Light Lower','Control',0,255,fn_pass)
cv2.createTrackbar('Light Upper','Control',0,255,fn_pass)

while(cap.isOpened()):
    ret, frame = cap.read()

    if not ret:
        break

    # Get slider values
    h_low = cv2.getTrackbarPos('Hue Lower','Control')//1
    h_upp = cv2.getTrackbarPos('Hue Upper','Control')//1
    s_low = cv2.getTrackbarPos('Sat Lower','Control')//1
    s_upp = cv2.getTrackbarPos('Sat Upper','Control')//1
    v_low = cv2.getTrackbarPos('Light Lower','Control')//1
    v_upp = cv2.getTrackbarPos('Light Upper','Control')//1

    small_frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)

    frame_hsv = cv2.cvtColor(small_frame, cv2.COLOR_RGB2HSV)

    lower_color_bound = np.array([h_low,s_low,v_low])
    upper_color_bound = np.array([h_upp,s_upp,v_upp])
    mask = cv2.inRange(frame_hsv, lower_color_bound, upper_color_bound)

    mask = cv2.erode(mask, None, iterations=7)
    mask = cv2.dilate(mask, None, iterations=7)

    res = cv2.bitwise_and(small_frame, small_frame, mask=mask)
    image, contours, hierarchy = cv2.findContours(mask,cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for cn in contours:
        (x,y),radius = cv2.minEnclosingCircle(cn)
        center = (int(x),int(y))
        radius = int(radius)
        res = cv2.circle(res,center,radius,(0,255,0),2)

    cv2.imshow('small_frame',small_frame)
    cv2.imshow('mask',mask)
    cv2.imshow('res',res)

    k = cv2.waitKey(200) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()
cap.release()