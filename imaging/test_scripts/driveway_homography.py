import cv2
import numpy as np

# 1. Define corresponding points (Source and Destination)
# Example: Mapping a rectangular source image to a custom 4-point shape in the destination
#TODO: not magic numbers - use driveway.jpg w and h
w = 118*2
h = 115+96+124
# pts_src = np.array([[1086, 1241], [2366, 1157], [4025, 1763], [196, 2521]], dtype=float)
pts_src = np.array([[1086, 1241], [2366, 1157], [4256, 1778], [196, 2521]], dtype=float)

pts_dst = np.array([[0, 0], [w, 0], [w, h], [0, h]], dtype=float)

# 2. Calculate the Homography Matrix
h_matrix, status = cv2.findHomography(pts_src, pts_dst)

# save the matrix
fs_write = cv2.FileStorage("homography.yaml", cv2.FILE_STORAGE_WRITE)
fs_write.write("homography", h_matrix)
fs_write.release()  # Always release the file stream
#how to unload
# fs_read = cv2.FileStorage("homography.yaml", cv2.FILE_STORAGE_READ)
# loaded_matrix = fs_read.getNode("homography").mat()
# fs_read.release()

# 3. Warp the Source Image
#TODO: get a prettier driveway image
img_src = cv2.imread('driveway_images\driveway.jpeg')
img_out = cv2.warpPerspective(img_src, h_matrix, (w, h))
cv2.imwrite('new_driveway.jpg', img_out)
