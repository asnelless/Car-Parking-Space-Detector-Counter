#manually detect the parking lots

#import necessary libraries
import cv2
import pickle

#declare the parameters of the rectangle
width,height = (158-50), (240-192)


#checks whether there are any parking lots
try:
    with open('CarParkPos','rb') as f:    #check if the file exists, then read it and add new positions
        List = pickle.load(f)
except:                                   #else create the file and add new positions
    List = []

#define a function that adds a rectangle whenever we click in the image
def mouse(click,x,y,flags,params):
    if click ==cv2.EVENT_LBUTTONDOWN:
        List.append((x,y))    #clicking left mouse button adds the rectangle 
    if click == cv2.EVENT_RBUTTONDOWN:
        for i, pos in enumerate(List):
            x1,y1 = pos
            if x1<x<x1+width and y1<y<y1+height:
                List.pop(i)   #clicking right mouse button on some rectangle deletes it
    #saves the created rectangles on the image in 'CarParkPos' file
    with open('CarParkPos','wb') as f:
        pickle.dump(List,f)

while True:
    image = cv2.imread('carParkImg.png')
    #create the rectangle using the parameters of the parking lot 
    cv2.rectangle(image, (50, 192), (158, 240), (255, 0, 255), 2)

    #for every position in the list, we put the rectangle over there
    for pos in List:
        cv2.rectangle(image,pos,(pos[0]+width,pos[1]+height),(255,0,255),2)
    cv2.imshow('Image', image)
    #undo the action if wrong place is selected 
    cv2.setMouseCallback('Image',mouse)

    cv2.waitKey(1)