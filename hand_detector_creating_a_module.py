import time
import cv2
import mediapipe as mp
import math
class handdetector:
    def __init__(self,mode=False ,max_hand=2 ,min_detect=0.5,min_track=0.5):
        self.static_image_mode =mode
        self.max_num_hands = max_hand
        self.min_detection_confidence =min_detect
        self.min_tracking_confidence = min_track

        self.mpHands = mp.solutions.hands
        self.hands =  self.mpHands.Hands(self.static_image_mode,self.max_num_hands
                                    ,self.min_detection_confidence,self.min_tracking_confidence)

        self.mpDraw = mp.solutions.drawing_utils
#--------------------------------So initialization is done now moving to hand detection part---------------------
    def findhands(self, img , draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.result = self.hands.process(imgRGB)
        if self.result.multi_hand_landmarks:
            for handLms in self.result.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms,
                                      self.mpHands.HAND_CONNECTIONS)
        return img

    def findPosition(self,img, handno=0 , draw = True):
                # This below code only prints the list of lm's uncomment if required
                self.lmlist=[]
                if self.result.multi_hand_landmarks:# if detects hand
                    myhands = self.result.multi_hand_landmarks[handno]  #asks for no of hands
                    for id, lm in enumerate(myhands.landmark):   #run this for given no of hands
                        h, w, c = img.shape

                        cx, cy = int(lm.x * w), int(lm.y * h)
                        # print(id, cx, cy)
                        self.lmlist.append([id , cx, cy])
                        if draw:
                            cv2.circle(img, (cx, cy), 8, (255, 0, 255), cv2.FILLED)
                return self.lmlist

    def findDistance(self,img,pt1,pt2,draw =True,r=10,t=3):    #pt1 and pt2 are the landmarks of which we want to find distance
        x1, y1 = self.lmlist[pt1][1:]
        x2, y2 = self.lmlist[pt2][1:]
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

        if draw:
            cv2.line(img, (x1, y1), (x2, y2), (0, 255, 0), t)
            cv2.circle(img, (x1, y1), r, (0, 255, 0), cv2.FILLED)
            cv2.circle(img, (x2, y2), r, (0, 255, 0), cv2.FILLED)
            cv2.circle(img, (cx, cy), r, (0, 255, 0), cv2.FILLED)  # for centre of line

        length = math.hypot((x2 - x1), (y2 - y1))

        return length,img,[x1,y1,x2,y2,cx,cy]



def main():
    pTime = 0
    cTime = 0
    vid = cv2.VideoCapture(1)
    detector = handdetector()
    while True:
        ret, img1 = vid.read()
        imgobj = detector.findhands(img1)
        lmlist = detector.findPosition(img1)
        if len(lmlist)!=0:
            length, imgobj2, coordinates = detector.findDistance(img1, 4, 8)
            print(lmlist[4])
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        cv2.putText(imgobj, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 3, (255, 0, 255), 3)

        cv2.imshow('camera', imgobj)
        cv2.waitKey(1)


if __name__ == "__main__":
    main()