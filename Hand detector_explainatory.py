# Mediapipe is the module developed by google and thats what we gonna use today
import time
import cv2
import mediapipe as mp
vid = cv2.VideoCapture(1)
mpHands = mp.solutions.hands   #thats some formality
hands = mpHands.Hands()  #  .Hands() method has some parameters but we want them all to be default
mpDraw = mp.solutions.drawing_utils  # This is a method provided by mediapipe to draw info of each hand
pTime =0
cTime =0

while True:
    ret , img =vid.read()

#     When the image file is read with the OpenCV function imread(), the order of colors is BGR (blue,    green, red). On the other hand, in Pillow, the order of colors is assumed to be RGB (red, green,   blue).
#     Therefore, if you want to use both the Pillow function and the OpenCV function, you need to         convert BGR and RGB.
# The Python Imaging Library is best suited for image archival and batch processing applications. Python pillow package can be used for creating thumbnails, converting from one format to another and print images, etc.
    imgRGB = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    result = hands.process(imgRGB)
# what is the use of .process()
# Processes an RGB image and returns the hand landmarks and handedness of each detected hand.

    # print(result.multi_hand_landmarks)   # detects landmarks if comes across the camera
    if result.multi_hand_landmarks:
        for handLms in result.multi_hand_landmarks:    # handLms is landmarks of a single hand
#           go to mpDraw
#---------------getting info within the hand---------------------------------------------------------
            # Each hand has its landmarks and corresponding id no.
            # landmarks give us the x and y coordinates
            # we also have their id numbers
            # and both of them are already listed in correct order
            for id , lm in enumerate(handLms.landmark):  #handLms.landmark is non-iterable
                # print(id ,"\n" ,lm)
                h,w,c= img.shape # c stands for channels if you dont understand channels reffer to "https://medium.com/featurepreneur/understanding-the-concept-of-channels-in-an-image-6d59d4dafaa9"

                cx ,cy = int(lm.x*w) , int(lm.y*h)
                print(id,cx,cy)
                #--------------------Drawing for a single id------------------------------------
                if id == 4:   # id 4 is for thumb tip
                    #also if we remove if statement it will run for all of them
                    cv2.circle(img,(cx,cy),15,(255,0,255),cv2.FILLED)


#----------------------------------------------------------------------------------------------------
            mpDraw.draw_landmarks(img,handLms,mpHands.HAND_CONNECTIONS)   # it draws landmarks for a single hand in frame
    #         also note that we are not giving RGB image as attribute i.e (imgRGB) instead we are using BGR image i.e. ('img) coz thats what we r going to display
#---------------Till nw we have drawn our hands with connections------------------------------------


#---------------------------Now we are setting FPS--------------------------------------------------
    cTime= time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime
    cv2.putText(img,str(int(fps)),(10,70),cv2.FONT_HERSHEY_SIMPLEX,3,(255,0,255),3)  #first three is for scale second 3 is for thickness  (10,70) defines the position


#-------------------So we are done setting our fps----------------------------------------------------







    cv2.imshow('camera', img)
    cv2.waitKey(1)


 # once we are done here we will move forward creating a module so it can come in handy use

def main():
    pTime = 0
    cTime = 0

    while True:
        ret, img = vid.read()



if __name__ =="__main__":
    main()