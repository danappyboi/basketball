import cv2
import numpy as np

# 1. Load reference target image and video
ref_img = cv2.imread('new_driveway.jpg', cv2.IMREAD_GRAYSCALE)
cap = cv2.VideoCapture('driveway_vid.mp4')

# 2. Initialize feature detector (ORB is fast and free)
orb = cv2.ORB_create(nfeatures=2000)
kp_ref, des_ref = orb.detectAndCompute(ref_img, None)

# Initialize Brute-Force Matcher for binary descriptors
bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
        
    # Convert current video frame to grayscale
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Find keypoints and descriptors in the video frame
    kp_frame, des_frame = orb.detectAndCompute(gray_frame, None)
    
    if des_frame is not None:
        # Match features between reference and frame
        matches = bf.match(des_ref, des_frame)
        # Sort matches by distance (best matches first)
        matches = sorted(matches, key=lambda x: x.distance)
        
        # Keep only the top matches (minimum 4 points required for homography)
        good_matches = matches[:50]
        
        if len(good_matches) >= 10:
            # Extract coordinates of matched points
            pts_ref = np.float32([kp_ref[m.queryIdx].pt for m in good_matches]).reshape(-1, 1, 2)
            pts_frame = np.float32([kp_frame[m.trainIdx].pt for m in good_matches]).reshape(-1, 1, 2)
            
            print(pts_ref, pts_frame)

            # Compute Homography matrix using RANSAC to filter out outlier mismatches
            H, mask = cv2.findHomography(pts_ref, pts_frame, cv2.RANSAC, 5.0)
            
            # Use the Homography matrix to warp an overlay image or find boundaries
            h, w = ref_img.shape
            corners = np.float32([[0, 0], [0, h-1], [w-1, h-1], [w-1, 0]]).reshape(-1, 1, 2)
            
            # Transform corners to frame space
            transformed_corners = cv2.perspectiveTransform(corners, H)
            
            # Draw the bounding box on the video frame
            frame = cv2.polylines(frame, [np.int32(transformed_corners)], True, (0, 255, 0), 3)
            
    cv2.imshow('Homography Video Tracking', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
