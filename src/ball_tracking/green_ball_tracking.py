#!/usr/bin/env python3

import argparse
import time
from collections import deque

import cv2
import imutils
import numpy as np
from imutils.video import VideoStream
from control_enum import Command as Cmd

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", help="path to the (optional) video file")
ap.add_argument("-b", "--buffer", type=int, default=64, help="max buffer size")
arguments = vars(ap.parse_args())

# define the lower and upper boundaries of the "green"
# ball in the HSV color space, then initialize the
# list of tracked points
# greenLower = (29, 86, 6)
# greenUpper = (64, 255, 255)
GREEN_LOWER = (30, 100, 40)
GREEN_UPPER = (90, 255, 255)
GREEN = (0, 255, 0)
OUTLINE = 2
pts = deque(maxlen=arguments["buffer"])

# if a video path was not supplied, grab the reference
# to the webcam
if not arguments.get("video", False):
    vs = VideoStream(src=0).start()
# otherwise, grab a reference to the video file
else:
    vs = cv2.VideoCapture(arguments["video"])
# allow the camera or video file to warm up
time.sleep(2.0)


class Exit(Exception):
    """A simple Exception to be risen when a quit signal is received."""
    def __init__(self, *args):
        super(Exit, self).__init__(*args)

    @staticmethod
    def quit():
        end()


def track():
    """Evalute the current frame and get the respective command for the server to follow."""
    # grab the current frame
    frame = vs.read()
    # handle the frame from VideoCapture or VideoStream
    frame = frame[1] if arguments.get("video", False) else frame
    # if we are viewing a video and we did not grab a frame,
    # then we have reached the end of the video
    if frame is None:
        raise Exit("Frame is None")

    # resize the frame, blur it, and convert it to the HSV
    # color space
    frame = imutils.resize(frame, width=600)
    blurred = cv2.GaussianBlur(frame, (15, 15), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

    height, width = frame.shape[:2]

    # construct a mask for the color "green", then perform
    # a series of dilations and erosions to remove any small
    # blobs left in the mask
    mask = cv2.inRange(hsv, GREEN_LOWER, GREEN_UPPER)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    # bounds of each trigger area relative to image dimensions
    RIGHT_BOUNDS = (
        (int(0.05 * width), int(0.25 * height)),
        (int(0.3 * width), int(0.75 * height))
    )
    LEFT_BOUNDS = (
        (int(0.7 * width), int(0.25 * height)),
        (int(0.95 * width), int(0.75 * height))
    )
    UPPER_BOUNDS = (
        (int(0.33 * width), int(0.05 * height)),
        (int(0.67 * width), int(0.35 * height))
    )
    LOWER_BOUNDS = (
        (int(0.33 * width), int(0.65 * height)),
        (int(0.67 * width), int(0.95 * height))
    )

    # Draw the rectangles to mark positions
    cv2.rectangle(frame, UPPER_BOUNDS[0], UPPER_BOUNDS[1], GREEN, OUTLINE)
    cv2.rectangle(frame, RIGHT_BOUNDS[0], RIGHT_BOUNDS[1], GREEN, OUTLINE)
    cv2.rectangle(frame, LOWER_BOUNDS[0], LOWER_BOUNDS[1], GREEN, OUTLINE)
    cv2.rectangle(frame,  LEFT_BOUNDS[0],  LEFT_BOUNDS[1], GREEN, OUTLINE)

    # find contours in the mask and initialize the current
    # (x, y) center of the ball
    mask_contours = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    mask_contours = imutils.grab_contours(mask_contours)
    center = None

    # only proceed if at least one contour was found
    if len(mask_contours) > 0:
        # find the largest contour in the mask, then use
        # it to compute the minimum enclosing circle and
        # centroid
        c = max(mask_contours, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

        # only proceed if the radius meets a minimum size
        if radius > 10:
            # draw the circle and centroid on the frame,
            # then update the list of tracked points
            cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)
            cv2.circle(frame, center, 5, (0, 0, 255), -1)

    # update the points queue
    pts.appendleft(center)

    # loop over the set of tracked points
    for i in range(1, len(pts)):
        # if either of the tracked points are None, ignore
        # them
        if pts[i - 1] is None or pts[i] is None:
            continue

        # otherwise, compute the thickness of the line and
        # draw the connecting lines
        thickness = int(np.sqrt(arguments["buffer"] / float(i + 1)) * 2.5)
        cv2.line(frame, pts[i - 1], pts[i], (0, 0, 255), thickness)

    # show the frame to our screen (flipped on y axis, so we see ourselves mirrored)
    cv2.imshow("Frame", cv2.flip(frame, 1))
    key = cv2.waitKey(1) & 0xFF

    # if the 'q' key is pressed, stop the loop
    if key == ord("q") or key == 27:
        raise Exit

    return positional_command(UPPER_BOUNDS, RIGHT_BOUNDS, LOWER_BOUNDS, LEFT_BOUNDS).value


def positional_command(upper, right, lower, left) -> Cmd:
    """Get the respective command according to the most recent ball positions."""
    xy = recent_mean()
    if xy is None:
        return Cmd.STOP
    if in_bounds(xy, upper):
        return Cmd.FORWARD
    if in_bounds(xy, right):
        return Cmd.RIGHT
    if in_bounds(xy, lower):
        return Cmd.BACKWARD
    if in_bounds(xy, left):
        return Cmd.LEFT
    return Cmd.STOP


def in_bounds(pt, rect):
    """
    Whether a point is within the bounds of a rectangle.
    Hereby a rectangle is a tuple of points and each point is a tuple of x and y.
    """
    x, y = pt
    if rect[0][0] < x <= rect[1][0] and rect[0][1] < y <= rect[1][1]:
        return True
    return False


def recent_mean():
    """The average point of the most recently tracked green ball positional points."""
    filtered = list(filter(lambda xy: xy is not None and None not in xy, pts))  # filter invalid values
    if len(filtered) < 20:  # make sure enough points are available
        return None
    recent = filtered[:len(filtered)//2]  # get only the more recent points
    x = y = 0
    for pt in recent:  # sum up x and y coordinates
        x += pt[0]
        y += pt[1]
    x //= len(recent)  # calculate their means
    y //= len(recent)
    return x, y


def end():
    """End the video evaluation."""
    # if we are not using a video file, stop the camera video stream
    if not arguments.get("video", False):
        vs.stop()
    # otherwise, release the camera
    else:
        vs.release()
    # close all windows
    cv2.destroyAllWindows()
