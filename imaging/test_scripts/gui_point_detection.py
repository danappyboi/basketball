#instead of doing homography every frame, we can track the corners of the
# driveway every frame and run the homography on those points

import cv2
import numpy as np
from collections import deque
from ultralytics import YOLO

court_w = 118*2
'''Width of the driveway in inches'''
court_h = 115+96+124
'''Height of the driveway in inches'''
queue = deque(maxlen=15) #TODO: test different queue sizes
'''A queue to store the last 15 points of the court '''

# Load the video file or webcam stream
cap = cv2.VideoCapture("driveway_vid.mp4")

# Parameters for Lucas-Kanade optical flow
lk_params = dict(
    winSize=(15, 15),
    maxLevel=2,
    criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03)
)

# Read the initial frame
ret, old_frame = cap.read()
if not ret:
    print("Failed to read video")
    cap.release()
    exit()

old_gray = cv2.cvtColor(old_frame, cv2.COLOR_BGR2GRAY)

model = YOLO("yolo26n.pt") 


# Initial point selection
# TODO: make this something that is done first by the user
og_p0 = np.array([[88, 186], [273, 150], [306, 367], [509, 193]], dtype=np.float32)
"""The original first 4 points"""
queue.append(og_p0)

p0 = og_p0.copy().reshape(-1, 1, 2) # needs to be reshaped for some reason, idk



def convert_to_homo(x, y, H) :
    '''Converts a point using the homography matrix `H`'''
    # convert to homogeneous
    homogeneous_point = np.array([x, y, 1.0])

    result = np.dot(H, homogeneous_point)

    # normalize by dividing by Z
    new_x = (int) (result[0] / result[2])
    new_y = (int) (result[1] / result[2])
    print((new_x, new_y))
    return (new_x, new_y)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Calculate sparse optical flow to find the new point coordinates
    p1, st, err = cv2.calcOpticalFlowPyrLK(old_gray, frame_gray, p0, None, **lk_params)

    # Select valid points (st == 1 means the point was successfully tracked)
    if p1 is not None:
        good_new = np.where(st == 1, p1.squeeze(axis=1), og_p0)
        good_old = p0

        #TODO: add corner detection, the corners are a good indication of where you should be
        # if the point goes too far from the og point, move it back
        for i in range(good_new.shape[0]):
            if np.linalg.norm(good_new[i] - np.mean(queue, axis=0)[i]) > 5:
                good_new[i] = np.mean(queue, axis=0)[i]
        
        queue.append(good_new)

        #TODO: set og_p0 to the avg of the past couplee points
        # if not flag:
        #     print(good_new)
        #     flag = True

        # draw the point
        for i, (new, old) in enumerate(zip(good_new, good_old)):
            a, b = new.ravel()
            c, d = old.ravel()
            
            frame = cv2.circle(frame, (int(a), int(b)), 5, (0,255,0), -1)
    
    
    #tracker stuff
    player_list = []

    results = model.track(frame_gray, persist=True, classes=[0], tracker="bytetrack.yaml")
    # Check if there are active detections/tracks
    if results[0].boxes.id is not None:
        boxes = results[0].boxes.xyxy.int().cpu().tolist()
        track_ids = results[0].boxes.id.int().cpu().tolist()

        # Annotate each tracked human on the frame using OpenCV
        for box, track_id in zip(boxes, track_ids):
            x1, y1, x2, y2 = box
            player_pt = ((x1+x2)/2, y2)
            player_list.append(player_pt)
            
            # Draw bounding box (Green)
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.circle(frame, center=(int(player_pt[0]), int(player_pt[1])), radius=5, color=(255, 0, 0), thickness=-1)
            
            # Display tracking ID text
            label = f"ID: {track_id}"
            cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
    

    # Showing the court view based on those tracked points
    pts_src = good_new
    pts_dst = np.float32([[0, 0], [court_w, 0], [0, court_h], [court_w, court_h]])
    H = cv2.getPerspectiveTransform(pts_src, pts_dst)
    court_frame = cv2.warpPerspective(frame, H, (court_w, court_h))
    
    for (x, y) in player_list:
        cv2.circle(court_frame, center=convert_to_homo(x, y, H), radius=5, color=(255, 0, 0), thickness=-1)

    # Show the newly tracked points
    cv2.imshow("Original View", frame)
    cv2.imshow('Court View', court_frame)


    # Break loop on 'ESC' key press
    if cv2.waitKey(30) & 0xFF == 27:
        break

    # Now update the previous frame and previous points
    old_gray = frame_gray.copy()
    p0 = good_new.reshape(-1, 1, 2)

cap.release()
cv2.destroyAllWindows()
