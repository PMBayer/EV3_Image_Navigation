#!/usr/bin/env python3

import cv2 as cv
import numpy as np

Debug = True  # Only relevant for debugging; turns on debug mode


# Method to compute the brightness of an image
# using the euclidean norm
# returns the brightness value of an Image
def compute_brightness(img):
    if len(img.shape) == 3:
        # Colored RGB or BGR (*Do Not* use HSV images with this function)
        # create brightness with euclidean norm
        return np.average(np.norm(img, axis=2)) / np.sqrt(3)
    else:
        # Grayscale
        return np.average(img)


# Method; that creates the skin mask of a given image
def skin_mask(img):
    hsvim = cv.cvtColor(img, cv.COLOR_BGR2HSV)
    lower = np.array([0, 48, 80], dtype="uint8")
    upper = np.array([20, 255, 255], dtype="uint8")
    skin_region_hsv = cv.inRange(hsvim, lower, upper)
    blurred = cv.blur(skin_region_hsv, (2, 2))
    ret, thresh = cv.threshold(blurred, 0, 255, cv.THRESH_BINARY)
    return thresh


# Method; to start the capture process
# Method uses cv2.VideoCapture
def capture(cap):
    # Setting up the camera; Tests its functionality
    if cap.isOpened():
        print("Capturing ...")
    else:
        print("Error open video")
    while cap.isOpened():
        ret, frame = cap.read()  # Liefert Erfolgswert und Videoframe
        if not ret:
            print("Error retrieving video frame")
            break

        height, width = frame.shape[:2]

        # shows an additional window with the masked skin;
        mask_img = skin_mask(frame)
        if Debug:
            cv.imshow("Skin", mask_img)

        # Draw the rectangles to mark positions;
        cv.rectangle(frame, (int(0.1 * width), int(0.6 * height)), (int(0.25 * width), int(0.8 * height)), (0, 255, 0),
                     3)
        cv.rectangle(frame, (int(0.75 * width), int(0.6 * height)), (int(0.9 * width), int(0.8 * height)), (0, 255, 0),
                     3)
        cv.rectangle(frame, (int(0.425 * width), int(0.2 * height)), (int(0.575 * width), int(0.4 * height)),
                     (0, 255, 0), 3)

        cv.imshow("Video", frame)  # Anzeige des Videoframes

        # Masking the Image;
        img_left = mask_img[int(0.6 * height):int(0.8 * height), int(0.1 * width):int(0.25 * width)]
        img_right = mask_img[int(0.6 * height):int(0.8 * height), int(0.75 * width):int(0.9 * width)]
        img_upper = mask_img[int(0.2 * height): int(0.4 * height), int(0.425 * width): int(0.575 * height)]

        # setting up the variables for decision tree; These variables contain the brightness values
        # of those parts of the image which are marked by the rectangles
        brightness_left = compute_brightness(img_left)
        brightness_right = compute_brightness(img_right)
        brightness_upper = compute_brightness(img_upper)

        # logging the brightness values for debugging purposes
        if Debug:
            print("Left:", brightness_left, "Right:", brightness_right, "Upper:", brightness_upper)

        # Decision Rule
        thresh_left = 100
        thresh_right = 100
        thresh_upper = 100

        return (evaluate_thresholds(brightness_left, brightness_right, thresh_left, thresh_right, brightness_upper,
                                    thresh_upper))


# Method: to evaluate the thresholds of an image mask
# returns: drive commands according to the evaluated thresholds
def evaluate_thresholds(brightness_left, brightness_right, thresh_left, thresh_right, brightness_upper, thresh_upper):
    # press ESC to end the session
    if cv.waitKey(1) == 27:
        print("End of session")
        return 'end'
    # drive forward
    elif (brightness_left > thresh_left) and (brightness_right > thresh_right) and (brightness_upper < thresh_upper):
        print("Both Hands")
        return 'forward'
    # drive backward
    elif brightness_upper > thresh_upper:
        print("Upper")
        return 'backward'
    # steer right
    elif (brightness_left > thresh_left) and (brightness_right < thresh_right) and (brightness_upper < thresh_upper):
        print("Right Hand")
        return 'right'
    # steer left
    elif (brightness_left < thresh_left) and (brightness_right > thresh_right) and (brightness_upper < thresh_upper):
        print("Left Hand")
        return 'left'
    # dont drive
    elif (brightness_left < thresh_left) and (brightness_right < thresh_right) and (brightness_upper < thresh_upper):
        print("No Hand")
        return 'stop'

# # only sending data if it has changed; comparing last and current identified command
# def update(data, counter):
#     if counter != 0:
#         if data[counter] != data[counter - 1]:
#             return True
#         else:
#             return False
#     else:
#         return True

# if __name__ == "__main__":
#     capture()
