#NOTE: this script works...ish, but it assumes the camera is static
import cv2
import numpy as np

cap = cv2.VideoCapture('driveway_vid.mp4')

tl = [646, 775]
tr = [1056, 396]
br = [553, 324]
bl = [169, 414]
ss_dim = (1342, 1009)
reg_dim = (640, 480)
x_ratio = reg_dim[0]/ss_dim[0]
y_ratio = reg_dim[1]/ss_dim[1]

tl = [tl[0] * x_ratio, tl[1] * y_ratio]
tr = [tr[0] * x_ratio, tr[1] * y_ratio]
br = [br[0] * x_ratio, br[1] * y_ratio]
bl = [bl[0] * x_ratio, bl[1] * y_ratio]

w = 118*2
h = 115+96+124

# Define 4 coordinates in your video frame that form a plane (e.g., a road surface)
pts_src = np.float32([tl, tr, bl, br])
# Define where those 4 coordinates should map in the output window
pts_dst = np.float32([[0, 0], [w, 0], [0, h], [w, h]])

# Calculate homography ONCE before processing frames
H = cv2.getPerspectiveTransform(pts_src, pts_dst)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    
    # Efficiently warp every frame using the same static matrix
    warped_frame = cv2.warpPerspective(frame, H, (w, h))
    
    cv2.imshow('Warped Perspective Feed', warped_frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
