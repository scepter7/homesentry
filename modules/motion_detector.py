import cv2
import numpy as np
import imutils

class MotionDetector:
    '''Motion Detection module.'''

    def __init__(self, minArea, deltaThresh, accumWeight=0.5):
        # Init camera stream, config file, frame accumulation weight,
        # min. area of detection, and fixed threshold
        self.accumWeight = accumWeight
        self.status = None

        self.minArea = minArea
        self.deltaThresh = deltaThresh

        # Init average background
        self.avg = None

    def update(self, image):
        # init set of locations, where motion is detected
        locs = []
        self.status = "Secure"

        # if background has not been initialized, init it
        if self.avg is None:
            self.avg = np.asfarray(np.copy(image))
            return locs

        # accumulate weighted average between current frame and avg. frame
        # get pixel-wise differences between current frame and avg. frame
        cv2.accumulateWeighted(image, self.avg, self.accumWeight)
        frameDelta = cv2.absdiff(image, cv2.convertScaleAbs(self.avg))

        # threshold the delta image and apply a series of dilations
        thresh = cv2.threshold(frameDelta, self.deltaThresh, 255,
            cv2.THRESH_BINARY)[1]
        thresh = cv2.dilate(thresh, None, iterations=2)

        # find contours in the dilated image
        (_, cnts, _) = cv2.findContours(np.copy(thresh), cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE)

        # if area of contour is bigger than min area - it's movement
        for c in cnts:
            if cv2.contourArea(c) > self.minArea:
                self.status = "Breached"
                locs.append(c)

        return locs
