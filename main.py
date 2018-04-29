from datetime import datetime
from threading import Thread
import time
import json
import requests
import numpy as np
import imutils
import cv2

from modules.camera import Camera
from modules.motion_detector import MotionDetector
from modules.alerter import Alerter


def alert(conf):
    '''Create an image with moving captured on it. Send it to Telegram Bot.'''
    a = Alerter()
    cv2.imwrite(a.path, frame)

    resp = requests.post(conf["url"], {"chat_id": conf["chat_id"]},
        files={'photo': ('{}.jpg'.format(a.name), open(a.path, 'rb'), 'image/jpg')})
    a.cleanup()
    if resp.status_code == 200:
        print("[INFO]Bot has been alerted")
    else:
        print("[ERROR]Could not send request to the bot. Error code: {}".format(resp.status_code))


if __name__ == "__main__":

    conf = json.load(open("config.json"))

    print("[INFO]Starting Camera...")
    vs = Camera(src=0).start()

    print("[INFO]Warming Up...")
    time.sleep(conf["camera_warmup"])

    print("[INFO]Initializing motion detectors...")
    camMotion = MotionDetector(conf["min_area"], conf["delta_thresh"])

    try:
        while True:

            frame = vs.read()
            frame = np.array(frame)

            frame = imutils.resize(frame, width=500)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            gray = cv2.GaussianBlur(gray, (21, 21), 0)
            locs = camMotion.update(gray)

            if len(locs) > 0:
                (minX, minY) = (np.inf, np.inf)
                (maxX, maxY) = (-np.inf, -np.inf)

                for l in locs:
                    (x, y, w, h) = cv2.boundingRect(l)
                    (minX, maxX) = (min(minX, x), max(maxX, x + w))
                    (minY, maxY) = (min(minY, y), max(maxY, y + h))

                cv2.rectangle(frame, (minX, minY), (maxX, maxY),
                    (0, 0, 255), 3)

            timestamp = datetime.now()
            ts = timestamp.strftime("%A %d %B %Y %I:%M:%S%p")

            cv2.putText(frame, "Perimeter Satus: {}".format(camMotion.status), (10, 20),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
            cv2.putText(frame, ts, (10, np.shape(frame)[0] - 10), cv2.FONT_HERSHEY_SIMPLEX,
                0.35, (0, 0, 255), 1)

            if camMotion.status == "Breached":
                t = Thread(target=alert, args=(conf,))
                t.start()

            if conf["is_streaming"] == True:
                cv2.imshow("Security Feed", frame)

            key = cv2.waitKey(1) & 0xFF
            if key == ord("q"):
                print("[INFO]Exitting...")
                break
    except KeyboardInterrupt:
        print("[INFO]Keyboard Interrupt detected. Stopping...")
    finally:
        print("[INFO]Cleaning up...")
        cv2.destroyAllWindows()
        vs.stop()
