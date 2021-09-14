import cv2
import time
import numpy as np
import hand_detector_creating_a_module as htm
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume


##########################################
# setiing var for dimensions of vid
wVid , hVid = 640 , 480
##########################################


vid = cv2.VideoCapture(1)
# setting vid height and width
vid.set(3,wVid)
vid.set(4,hVid)
detector = htm.handdetector(min_detect=0.8)
pTime=0
vol =0
volBar = 0
volPer = 0

# ----------------------There are many libraries that we can use to change volume--------------------------------
# ----------------------Here we are using pycaw from github------------------------------------------------------
# ----------------------pip install pycaw------------------------------------------------------------------------

##############pycaw usage template###############################################
#____________these seems like initialisations we dont change them--------------
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
#_______________________________________________________________________________

# volume.GetMute()   We dont want that now later try it on your own
# volume.GetMasterVolumeLevel()     We dont want that now later try it on your own
VolRng = volume.GetVolumeRange()     # range -95 to 0   0 is max

minVol = VolRng[0]  #indexing VolRng
maxVol = VolRng[1]  #indexing VolRng


#################################################################################





while True:
    success , img = vid.read()
    #--------------setting up fps--------------------------
    cTime = time.time()
    fps= 1/(cTime-pTime)
    pTime= cTime

    cv2.putText(img,f"FPS:{int(fps)}",(10,50),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2)
    #------------------------------------------------------
    imgobj=detector.findhands(img)
    lmlist=detector.findPosition(img,draw=False)
    if len(lmlist) !=0:
        # print(lmlist[4],lmlist[8])
        #-------------------------now we make circle on the required lanmarks--------------------------------------------
        x1 , y1 = lmlist[4][1], lmlist[4][2]
        x2 , y2 = lmlist[8][1], lmlist[8][2]
        cx , cy =(x1+x2)//2 , (y1+y2)//2   # denotes the x and y of centre   also throws error if we only use single /
        cv2.circle(img,(x1 ,y1),10,(0,255,0),cv2.FILLED)
        cv2.circle(img,(x2,y2),10,(0,255,0),cv2.FILLED)

        #---------------------------------------------------------------------------------------------------------------

        #------------------------------Now we create a line between these two lms---------------------------------------
        cv2.line(img ,(x1,y1), (x2,y2) , (0,255,0),3)
        #-----Finding the centre of the line-----------------------------
        cv2.circle(img, (cx, cy), 10, (0, 255, 0), cv2.FILLED)
        #----------------------------------------------------------------
        #---------------------------------------------------------------------------------------------------------------
        #-------------------------------Finding the length of the line--------------------------------------------------
        # we can either do our complicated math here or we can simply use function already given in python
        length = math.hypot((x2-x1),(y2-y1))
        print(length)
        # our hand range was from 240 to 30
        # our vol range was from 0 to -95
        # so we want to convert our hand range to our volume range
        vol = np.interp(length,[15,230],[minVol,maxVol])   # .interp is function of numpy   google it

        print(vol)
        volume.SetMasterVolumeLevel(vol, None)  # sets the volume
        # volume.SetMasterVolumeLevel is originally from pycaw project we just copy pasted it here

        if length < 50:
            cv2.circle(img, (cx, cy), 10, (255, 255, 255), cv2.FILLED)#changes centre color when if statement satisfied

        #------------------Till now we done with our work but we can adittionally add a rectangle bar to show our volume
        volBar =  np.interp(length,[15,230],[400,120]) #again changing range for vaolume bar
        volPer = np.interp(length,[15,230],[0,100])
        cv2.rectangle(img,(30,120),(85,400),(0,255,0),3)
        cv2.rectangle(img,(30,int(volBar)),(85,400),(0,255,0),cv2.FILLED)
        cv2.putText(img , f"{int(volPer)}%",(30,450),cv2.FONT_HERSHEY_PLAIN,2,(0,0,255),3)



    cv2.imshow('img', img)
    cv2.waitKey(1)


