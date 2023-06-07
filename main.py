#importing necessary libraries
import cv2
import numpy as np
import cvzone
import pickle  #saves the places that was selected on the picture

cap = cv2.VideoCapture('carPark.mp4')

with open('CarParkPos', 'rb') as f:
    List = pickle.load(f)
width,height = (158-50), (240-192)


def checkParkingSpace(imagePro):
    spaceCounter = 0
    for pos in List:

        x,y = pos
        cv2.imshow('Image', img)

        imgCrop = imagePro[y:y+height,x:x+width]
        cv2.imshow(str(x*y),imgCrop)
        count = cv2.countNonZero(imgCrop)
        cvzone.putTextRect(img,str(count),(x,y+height-2),scale=1,thickness=2,offset=0,colorR=(0,0,255))
        if count < 500:
            color = (0,255,0) #BGR
            thickness = 5
            spaceCounter +=1
        else:
            color = (0,0,255)
            thickness = 2
        cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height), color, thickness)
    cvzone.putTextRect(img,f'FREE{str(spaceCounter)}/{len(List)}',(450,50),scale=2,thickness=5,offset=20,colorR=(0,200,0))

while True:
    #loop the video
    if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)



    success, img = cap.read()

    imgGray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray,(3,3),1)
    imgThreshold = cv2.adaptiveThreshold(imgBlur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                          cv2.THRESH_BINARY_INV,25,16)

    imgMedian = cv2.medianBlur(imgThreshold,5)
    kernel = np.zeros((3,3),np.uint8)
    imgDilate = cv2.dilate(imgMedian,kernel,iterations=1)


    checkParkingSpace(imgDilate)

    cv2.imshow('Image',img)
    cv2.waitKey(1)