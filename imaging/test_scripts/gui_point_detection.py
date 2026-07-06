#instead of doing homography every frame, we can track the corners of the
# driveway every frame and run the homography on those points

import cv2
import numpy as np

# Load the video file or webcam stream
cap = cv2.VideoCapture("driveway_vid.mp4")

# Parameters for Lucas-Kanade optical flow
lk_params = dict(
    winSize=(15, 15),
    maxLevel=2,
    criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03)
)

# Create random colors for drawing tracking trajectories
color = np.random.randint(0, 255, (100, 3))

# Read the initial frame
ret, old_frame = cap.read()
if not ret:
    print("Failed to read video")
    cap.release()
    exit()

old_gray = cv2.cvtColor(old_frame, cv2.COLOR_BGR2GRAY)

# --- Point Initialization ---
# Option A: Automatically find sharp corner points to track
# p0 = cv2.goodFeaturesToTrack(old_gray, maxCorners=100, qualityLevel=0.3, minDistance=7, blockSize=7)

# Option B: Uncomment below to define your own specific coordinates (X, Y) manually
og_p0 = np.array([[88, 186], [273, 150], [509, 193], [306, 367]], dtype=np.float32)
p0 = og_p0.copy().reshape(-1, 1, 2)

# Create a blank mask array to draw the historical tracking lines
mask = np.zeros_like(old_frame)

flag = False

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

        for i in range(good_new.shape[0]):
            if np.linalg.norm(good_new[i] - og_p0[i]) > 20:
                good_new = og_p0

        # if not flag:
        #     print(good_new)
        #     flag = True

        # Draw the tracking trajectories
        for i, (new, old) in enumerate(zip(good_new, good_old)):

            a, b = new.ravel()
            c, d = old.ravel()
            
            # Draw lines connecting the old coordinates to the new coordinates
            # mask = cv2.line(mask, (int(a), int(b)), (int(c), int(d)), (0, 255, 0), 2)
            frame = cv2.circle(frame, (int(a), int(b)), 5, (0,255,0), -1)

    img = cv2.add(frame, mask)

    cv2.imshow("Point Tracking (Lucas-Kanade)", img)

    # Break loop on 'ESC' key press
    if cv2.waitKey(30) & 0xFF == 27:
        break

    # Now update the previous frame and previous points
    old_gray = frame_gray.copy()
    p0 = good_new.reshape(-1, 1, 2)

cap.release()
cv2.destroyAllWindows()
