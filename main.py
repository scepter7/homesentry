import argparse
from datetime import datetime
from tempimage import TempImage
import imutils
import json
import time
import requests
import numpy as np
import cv2


ap = argparse.ArgumentParser()
ap.add_argument("-c", "--conf", required=True,
    help="Path to the JSON configuration file")
args = vars(ap.parse_args())


conf = json.load(open(args["conf"]))
camera = cv2.VideoCapture(0)
camera.set(cv2.CAP_PROP_FPS, 10)


print("[INFO]Warming Up...")
time.sleep(conf["camera_warmup"])
avg = None
lastUploaded = datetime.now()
motionCounter = 0


while True:
    (grabbed, frame) = camera.read()
    if not grabbed:
        print("[ERROR]Could not grab frame. Exitting...")
        break
    

    frame = np.array(frame)
    timestamp = datetime.now()
    text = "Secure"


    frame = imutils.resize(frame, width=500)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)


    if avg is None:
        print("[INFO]Starting background model...")
        avg = np.asfarray(np.copy(gray))
        continue
    

    cv2.accumulateWeighted(gray, avg, 0.5)
    frameDelta = cv2.absdiff(gray, cv2.convertScaleAbs(avg))


    thresh = cv2.threshold(frameDelta, conf["delta_thresh"], 255,
        cv2.THRESH_BINARY)[1]
    thresh = cv2.dilate(thresh, None, iterations=2)
    (_, cnts, _) = cv2.findContours(np.copy(thresh), cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)

    
    for c in cnts:
        if cv2.contourArea(c) < conf["min_area"]:
            continue

        (x, y, w, h) = cv2.boundingRect(c)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        text = "Breached"
    

    ts = timestamp.strftime("%A %d %B %Y %I:%M:%S%p")
    cv2.putText(frame, "Perimeter Status: {}".format(text), (10, 20),
        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    cv2.putText(frame, ts, (10, np.shape(frame)[0] - 10), cv2.FONT_HERSHEY_SIMPLEX,
        0.35, (0, 0, 255), 1)

    
    if text == "Breached":
        if (timestamp - lastUploaded).seconds >= conf["min_upload_seconds"]:
            motionCounter += 1

            if motionCounter >= conf["min_motion_frames"]:
                t = TempImage()
                cv2.imwrite(t.path, frame)

                print("[INFO] - [{}] Breach has been detected! Sending to Bot...".format(ts))
                response = requests.post(conf["url"], {"chat_id": conf["chat_id"]},
                    files={'photo': ('{}.jpg'.format(t.name), open(t.path, 'rb'), 'image/jpg')})
                t.cleanup()
    else:
        motionCounter = 0


    cv2.imshow("Security Feed", frame)
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        print("[INFO]Exitting...")
        break


print("[INFO]Cleaning up...")
camera.release()
cv2.destroyAllWindows()
