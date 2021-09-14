import time
import cv2
import mediapipe as mp
import hand_detector_creating_a_module as hd
pTime = 0
cTime = 0
vid = cv2.VideoCapture(1)
detector = hd.handdetector()
while True:
    ret, img1 = vid.read()
    imgobj = detector.findhands(img1)
    lmlist = detector.findPosition(img1)
    if len(lmlist) != 0:
        print(lmlist[4])
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(imgobj, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 3, (255, 0, 255), 3)
    cv2.imshow('camera', imgobj)
    cv2.waitKey(1)
