import cv2
import numpy as np

# 1. Define dimensions (Height, Width, Channels)
# For a color image, channels = 3 (Blue, Green, Red)
height, width, channels = 400, (118*2), 3 #based on the measurements taken

# 2. Create a solid black image (zeros)
# Use uint8 (unsigned 8-bit integer) for standard images
image = np.zeros((height, width, channels), dtype=np.uint8)

# 3. Optional: Make it a white canvas instead
# image.fill(255) 

# 4. Save or display the image
cv2.imwrite('new_image.jpg', image)
cv2.imshow('Canvas', image)
cv2.waitKey(0)
cv2.destroyAllWindows()
