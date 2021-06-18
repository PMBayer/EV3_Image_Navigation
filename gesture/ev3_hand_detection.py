#!/usr/bin/env python3

import cv2 as cv
import numpy as np
from cv2 import norm

Debug = True


def compute_brightness(img):
    if len(img.shape) == 3:
        # Colored RGB or BGR (*Do Not* use HSV images with this function)
        # create brightness with euclidean norm
        return np.average(np.norm(img, axis=2)) / np.sqrt(3)
    else:
        # Grayscale
        return np.average(img)


def skin_mask(img):
    hsvim = cv.cvtColor(img, cv.COLOR_BGR2HSV)
    lower = np.array([0, 48, 80], dtype="uint8")
    upper = np.array([20, 255, 255], dtype="uint8")
    skin_region_hsv = cv.inRange(hsvim, lower, upper)
    blurred = cv.blur(skin_region_hsv, (2, 2))
    ret, thresh = cv.threshold(blurred, 0, 255, cv.THRESH_BINARY)
    return thresh


def capture():
    cap = cv.VideoCapture(0)
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
        # print(width," x ", height)

        mask_img = skin_mask(frame)
        if Debug:
            cv.imshow("Skin", mask_img)

        cv.rectangle(frame, (int(0.1 * width), int(0.6 * height)), (int(0.25 * width), int(0.8 * height)), (0, 255, 0),
                     3)
        cv.rectangle(frame, (int(0.75 * width), int(0.6 * height)), (int(0.9 * width), int(0.8 * height)), (0, 255, 0),
                     3)
        cv.imshow("Video", frame)  # Anzeige des Videoframes

        img_left = mask_img[int(0.6 * height):int(0.8 * height), int(0.1 * width):int(0.25 * width)]
        img_right = mask_img[int(0.6 * height):int(0.8 * height), int(0.75 * width):int(0.9 * width)]

        brightness_left = compute_brightness(img_left)
        brightness_right = compute_brightness(img_right)

        if Debug:
            print("Left:", brightness_left, "Right:", brightness_right)

        # Decision Rule
        thresh_left = 100
        thresh_right = 100

        if cv.waitKey(1) == 27:
            break  # Wait for Esc

        return evaluate_thresholds(brightness_left, brightness_right, thresh_left, thresh_right)


def evaluate_thresholds(brightness_left, brightness_right, thresh_left, thresh_right):
    if (brightness_left > thresh_left) and (brightness_right > thresh_right):
        print("Both Hands")
        return 2
    if (brightness_left > thresh_left) and (brightness_right < thresh_right):
        print("Right Hand")
        return 4
    if (brightness_left < thresh_left) and (brightness_right > thresh_right):
        print("Left Hand")
        return 3
    if (brightness_left < thresh_left) and (brightness_right < thresh_right):
        print("No Hand")
        return 1
