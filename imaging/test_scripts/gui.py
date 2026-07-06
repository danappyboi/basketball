import cv2
import numpy as np

WINDOW_NAME = "Basketball GUI"
CIRCLE_RADIUS = 10
CIRCLE_COLOR = (0, 255, 0)
CIRCLE_THICKNESS = 2

# in order to fit onto the screen, resize the driveway image to (800,600)
big_img = cv2.imread('driveway_images\driveway.jpeg')
dim = (800, 600)
x_ratio = big_img.shape[1]/dim[0]
y_ratio = big_img.shape[0]/dim[1]

left_img = cv2.resize(big_img, dim, interpolation=cv2.INTER_LINEAR)
right_img = cv2.imread('new_driveway.jpg')

# load the matrix back
fs_read = cv2.FileStorage("homography.yaml", cv2.FILE_STORAGE_READ)
h_matrix = fs_read.getNode("homography").mat()
fs_read.release()

# i couldn't tell you what these next two functions do, just that they work
def pad_to_height(image, height):
    if image.shape[0] >= height:
        return image
    pad_bottom = height - image.shape[0]
    return cv2.copyMakeBorder(image, 0, pad_bottom, 0, 0, cv2.BORDER_CONSTANT, value=(0, 0, 0))

def combine_images(left, right):
    target_height = max(left.shape[0], right.shape[0])
    left_padded = pad_to_height(left, target_height)
    right_padded = pad_to_height(right, target_height)
    return np.hstack((left_padded, right_padded))


display_image = combine_images(left_img.copy(), right_img.copy())
"""The image that gets displayed by the GUI is the left image next to the 
right image"""

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

def click_handler(event, x, y, flags, params):
    if event != cv2.EVENT_LBUTTONDOWN:
        return

    if x < left_img.shape[1] and y < left_img.shape[0]:
        cv2.circle(left_img, (x, y), CIRCLE_RADIUS, CIRCLE_COLOR, CIRCLE_THICKNESS)
        cv2.circle(right_img, convert_to_homo(x * x_ratio, y * y_ratio, h_matrix), 
                   CIRCLE_RADIUS, CIRCLE_COLOR, CIRCLE_THICKNESS)
        display_img = combine_images(left_img, right_img)
        cv2.imshow(WINDOW_NAME, display_img)

cv2.namedWindow(WINDOW_NAME, cv2.WINDOW_AUTOSIZE)
cv2.setMouseCallback(WINDOW_NAME, click_handler)
cv2.imshow(WINDOW_NAME, display_image)

while True:
    key = cv2.waitKey(20) & 0xFF
    if key == 27 or key == ord("q"):
        break

cv2.destroyAllWindows()