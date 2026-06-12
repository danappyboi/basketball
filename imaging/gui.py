import argparse
import os

import cv2
import numpy as np

WINDOW_NAME = "Two Image Viewer"
CIRCLE_RADIUS = 10
CIRCLE_COLOR = (0, 255, 0)
CIRCLE_THICKNESS = 2

big_left_img = cv2.imread('driveway_images\driveway.jpeg')

dimensions = (800, 600)
left_img = cv2.resize(big_left_img, dimensions, interpolation=cv2.INTER_LINEAR)
right_img = cv2.imread('new_driveway.jpg')
x_ratio = 4032/800
y_ratio = 3024/600

# 3. Load the matrix back
fs_read = cv2.FileStorage("homography.yaml", cv2.FILE_STORAGE_READ)
h_matrix = fs_read.getNode("homography").mat()
fs_read.release()


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

def convert_to_homo(x, y, H) :
    # Sample 3x3 homography matrix and point
    # H = np.eye(3, dtype=np.float32)

    # 1. Convert to homogeneous coordinates by adding a 1: [x, y, 1]
    homogeneous_point = np.array([x, y, 1.0])

    # 2. Multiply the Homography matrix by the point
    # Resulting vector will look like: [x_prime, y_prime, z_prime]
    result = np.dot(H, homogeneous_point)

    # 3. Normalize by dividing by the third element (Z) to get final 2D coordinates
    new_x = (int) (result[0] / result[2])
    new_y = (int) (result[1] / result[2])
    print((new_x, new_y))
    return (new_x, new_y)

def click_handler(event, x, y, flags, params):
    if event != cv2.EVENT_LBUTTONDOWN:
        return

    if x < left_img.shape[1] and y < left_img.shape[0]:
        cv2.circle(left_img, (x, y), CIRCLE_RADIUS, CIRCLE_COLOR, CIRCLE_THICKNESS)
        cv2.circle(right_img, convert_to_homo(x * x_ratio, y * y_ratio, h_matrix), CIRCLE_RADIUS, CIRCLE_COLOR, CIRCLE_THICKNESS)
        display_img = combine_images(left_img, right_img)
        cv2.imshow(WINDOW_NAME, display_img)


# def parse_args():
#     parser = argparse.ArgumentParser(description="Show two images side-by-side and draw a circle where you click on the left image.")
#     parser.add_argument("left_image", nargs="?", default=None, help="Path to the left image")
#     parser.add_argument("right_image", nargs="?", default=None, help="Path to the right image")
#     return parser.parse_args()


# def main():
    # left_image = load_image(args.left_image, "Missing Left Image")
    # right_image = load_image(args.right_image, "Missing Right Image")

    # display_image = combine_images(left_image.copy(), right_image.copy())

    # state = {
    #     "left_image": left_image,
    #     "right_image": right_image,
    #     "display_image": display_image,
    #     "left_width": left_image.shape[1],
    #     "left_height": left_image.shape[0],
    #     "radius": CIRCLE_RADIUS,
    #     "color": CIRCLE_COLOR,
    #     "thickness": CIRCLE_THICKNESS,
    # }

cv2.namedWindow(WINDOW_NAME, cv2.WINDOW_AUTOSIZE)
cv2.setMouseCallback(WINDOW_NAME, click_handler)
cv2.imshow(WINDOW_NAME, display_image)

while True:
    key = cv2.waitKey(20) & 0xFF
    if key == 27 or key == ord("q"):
        break

cv2.destroyAllWindows()


# if __name__ == "__main__":
#     main()
