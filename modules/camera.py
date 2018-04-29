from threading import Thread
import cv2

class Camera:
    '''Camera module.'''

    def __init__(self, src=0):
        # Initialize videostream from source
        self.stream = cv2.VideoCapture(src)

        # Read first frame
        (self.grabbed, self.frame) = self.stream.read()

        # Indicate whether the stream should be stopped
        self.stopped = False

    def start(self):
        # Read frames from stream
        Thread(target=self.update, args=()).start()
        return self

    def update(self):
        # Keep getting frames until stop command is requested
        while True:
            if self.stopped:
                return
            (self.grabbed, self.frame) = self.stream.read()

    def read(self):
        # Get frame
        return self.frame

    def stop(self):
        # Command to stop the videostream
        self.stopped = True
