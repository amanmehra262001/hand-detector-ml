import pyautogui   # documentation at https://pyautogui.readthedocs.io/en/latest/
import hand_detector_creating_a_module as htm
import time
import numpy as np
import cv2


######################################
Hvid , Wvid = 480 , 640
Hscr , Wscr = pyautogui.size()
FrameR = 50 #Frame Reduction
smoothening = 7
######################################
pTime = 0
PlocX ,PlocY =0,0   # previous location
ClocX ,ClocY =0,0   # current location

vid = cv2.VideoCapture(1)
vid.set(3, Hvid)
vid.set(4, Wvid)


detector = htm.handdetector(min_detect=0.85,max_hand=1)


while True:
    success , img = vid.read()
# 1. Finding hands landmarks
    imgobj = detector.findhands(img)
    lmlist = detector.findPosition(img,draw = False)
    # print(lmlist)
# 2. tip of index and middle finger
    if len(lmlist) !=0:
        x1,y1= lmlist[8][1:]
        x2,y2= lmlist[12][1:]
        cv2.rectangle(img, (FrameR, FrameR), (Wvid - FrameR, Hvid - FrameR), (255, 0, 255), 2)
        cv2.circle(img,(x2,y2),13,(255,0,255),cv2.FILLED)
# 3. check which fingers are up
        fingers = detector.fingerup()
    # print(fingers)
# 4. if only index fingers are up : move
        if fingers[1] == 1 and fingers[2] == 0:
            # print("index up")
# 5. convert coordinates
            x3 = np.interp(x1,(FrameR,Wvid-FrameR),(FrameR,Wscr))
            y3 = np.interp(x1,(FrameR,Hvid-FrameR),(FrameR,Hscr))
            cv2.circle(img, (x1, y1), 13, (255, 0, 255), cv2.FILLED)
# 6. smoothen values    (we'll dilute it a little bit)
            ClocX = PlocX + (x3 - PlocX)/smoothening
            ClocY = PlocY + (y3 - PlocY)/smoothening
# 7. move mouse
            pyautogui.moveTo(Wscr-ClocX ,Hscr-ClocY)
            PlocX ,PlocY =ClocX ,ClocY
# 8. both index and middle finger are up : click
        if fingers[1] == 1 and fingers[2] == 1:
# 9. find distance between fingers
            length, img ,lminfo  =detector.findDistance(img, 8, 12)
            # print(length)
#10. click mouse if distance is short
            if length<5:
                cv2.circle(img, (lminfo[4], lminfo[5]), 13, (255,255,255), cv2.FILLED)
                pyautogui.click()
#11.Showing FPS
    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime
    cv2.putText(img,str(int(fps)),(10,40),cv2.FONT_HERSHEY_PLAIN,3,(255,0,0),2)
#12. display
    cv2.imshow("camera",img)
    cv2.waitKey(1)

