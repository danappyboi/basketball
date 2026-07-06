#NOTE: this was written by AI and is dogshit. used it to make gui

import argparse
import os

import cv2
import numpy as np

WINDOW_NAME = "Two Image Viewer"
CIRCLE_RADIUS = 10
CIRCLE_COLOR = (0, 255, 0)
CIRCLE_THICKNESS = 2


def load_image(path, fallback_text, size=(640, 480)):
    if path and os.path.isfile(path):
        image = cv2.imread(path)
        if image is not None:
            return image

    image = np.full((size[1], size[0], 3), 40, dtype=np.uint8)
    cv2.putText(
        image,
        fallback_text,
        (20, size[1] // 2),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (220, 220, 220),
        2,
        cv2.LINE_AA,
    )
    return image


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


def click_handler(event, x, y, flags, param):
    state = param
    if event != cv2.EVENT_LBUTTONDOWN:
        return

    if x < state["left_width"] and y < state["left_height"]:
        cv2.circle(state["left_image"], (x, y), state["radius"], state["color"], state["thickness"])
        state["display_image"] = combine_images(state["left_image"], state["right_image"])
        cv2.imshow(WINDOW_NAME, state["display_image"])


def parse_args():
    parser = argparse.ArgumentParser(description="Show two images side-by-side and draw a circle where you click on the left image.")
    parser.add_argument("left_image", nargs="?", default=None, help="Path to the left image")
    parser.add_argument("right_image", nargs="?", default=None, help="Path to the right image")
    return parser.parse_args()


def main():
    args = parse_args()
    left_image = load_image(args.left_image, "Missing Left Image")
    right_image = load_image(args.right_image, "Missing Right Image")

    display_image = combine_images(left_image.copy(), right_image.copy())

    state = {
        "left_image": left_image,
        "right_image": right_image,
        "display_image": display_image,
        "left_width": left_image.shape[1],
        "left_height": left_image.shape[0],
        "radius": CIRCLE_RADIUS,
        "color": CIRCLE_COLOR,
        "thickness": CIRCLE_THICKNESS,
    }

    cv2.namedWindow(WINDOW_NAME, cv2.WINDOW_AUTOSIZE)
    cv2.setMouseCallback(WINDOW_NAME, click_handler, state)
    cv2.imshow(WINDOW_NAME, display_image)

    while True:
        key = cv2.waitKey(20) & 0xFF
        if key == 27 or key == ord("q"):
            break

    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
