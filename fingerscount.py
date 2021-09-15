import cv2
import time
import os
import hand_detector_creating_a_module as htm


wcam , hcam = 640,480

vid = cv2.VideoCapture(1)
vid.set(3,wcam)
vid.set(4,hcam)
pTime=0

# since our all the images of fingers are going to flot on our camera screen so here we named a list as overlay and import all the images there by following method using a for loop. here our os module came into play.
folderpath = "fingers"
mylist = os.listdir(folderpath)
# print(mylist)
overlay = []
for images in mylist:
    image = cv2.imread(f"{folderpath}/{images}")
    overlay.append(image)
# print(len(overlay))

#-------------------Below code was written by me to check h,w,c for all images in the folder--------
# for id in range(0, 6):
#     h,w,c=overlay[id].shape
# max shape came out to be 200*202
#-----------------------------------------------------------------------------------------------------

detector = htm.handdetector(min_detect=0.8)
tipId=[4,8,12,16,20]
while True:
    success , img = vid.read()
    imgobj = detector.findhands(img)
    lmlist = detector.findPosition(img,draw=False)
    # print(lmlist)
    fingers= []
    if len(lmlist) !=0:
        if lmlist[tipId[0]][1]<lmlist[tipId[0]-1][1]:
            fingers.append(1)
        else:
            fingers.append(0)
        for id in range(1,5):
            if lmlist[tipId[id]][2]<lmlist[tipId[id]-2][2]:
                fingers.append(1)
            else:
                fingers.append(0)
    # print(fingers)
        totalfingers = fingers.count(1)
        # print(totalfingers)





# once our overlay list is formed we overlay it on our image . As we know image is also a matrix so what we do is slicing the matrix to put overlaying image.

    # for image_no in range(0, 6):
        h, w, c = overlay[totalfingers-1].shape #we have taken this code from above that was created by me;)
        img[0:h,0:w] = overlay[totalfingers-1]



        cv2.rectangle(img, (10,250),(150,400),(255,0,255),cv2.FILLED)
        cv2.putText(img ,str(totalfingers),(35,375),cv2.FONT_HERSHEY_PLAIN,8,(255,0,0),5)

    # displaying fps
    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime
    cv2.putText(img,f"FPS: {int(fps)}",(480,25),cv2.FONT_HERSHEY_PLAIN,2,(0,255,0),2)




    cv2.imshow('camera', img)
    cv2.waitKey(1)