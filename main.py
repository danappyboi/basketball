import cv2 as cv
import numpy as np

cap = cv.VideoCapture(0)


while(1):

    # Take each frame
    _, frame = cap.read()

    # Convert BGR to HSV
    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

    # define ranges of red color in HSV
    lower_red = np.array([0,152,126])
    upper_red = np.array([10,255,255])

    lower_violet = np.array([163, 50, 0])
    upper_violet = np.array([180, 255, 255])

    # Add the masks together
    mask_red = cv.inRange(hsv, lower_red, upper_red)
    mask_violet = cv.inRange(hsv, lower_violet, upper_violet)
    mask = cv.add(mask_red, mask_violet)

    # Bitwise-AND mask and original image
    res = cv.bitwise_and(frame,frame, mask= mask)


    #getting the center of the mask
    contours, hierarchy = cv.findContours(mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

    #theres two ways to do this: could get a weighted avg, or get
    #the biggest area contour. Rn it gets biggest area, but the code
    #for weighted avg is there too.

    max_area = -1
    max_cont = 0
    # x_list = []
    # y_list = []
    # areas = []
    for contour in contours:
        area = cv.contourArea(contour)
        M = cv.moments(contour)

        if area > max_area:
            max_area = area
            max_cont = contour

    #     if M['m00'] != 0:
    #         cx = int(M['m10'] / M['m00'])
    #         cy = int(M['m01'] / M['m00'])
    #         x_list.append(cx)
    #         y_list.append(cy)
    #         areas.append(area)

    # if sum(areas) != 0:       
    #     avg_x = int(np.average(x_list, weights=areas))
    #     avg_y = int(np.average(y_list, weights=areas))
    #     print((avg_x, avg_y))
    #     cv.circle(frame, (avg_x, avg_y), 10, (255, 255, 255), -1)

    M = cv.moments(max_cont)
    if M['m00'] != 0:
        cx = int(M['m10'] / M['m00'])
        cy = int(M['m01'] / M['m00']) 
        cv.circle(frame, (cx, cy), 10, (255, 0, 0), -1)

    cv.imshow('frame',frame)
    cv.imshow('mask',mask)
    cv.imshow('res',res)
    k = cv.waitKey(5) & 0xFF
    if k == 27:
        break


cv.destroyAllWindows()