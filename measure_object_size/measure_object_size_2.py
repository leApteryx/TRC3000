from re import T
import cv2
from object_detector import*
import numpy as np

#Load Aruco detector
parameters=cv2.aruco.DetectorParameters_create()
aruco_dict=cv2.aruco.Dictionary_get(cv2.aruco.DICT_5X5_50)


#load object detector
detector=HomogeneousBgDetector()

#Load cam_image
cap=cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH,1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT,720)

while True:
    _,img=cap.read()


    #Get aruco marker
    corners, _, _=cv2.aruco.detectMarkers(img, aruco_dict, parameters=parameters)
    #Draw boundary around marker
    int_corners=np.int0(corners)
    cv2.polylines(img, int_corners,True,(0,255,0),5)

    #Aruco perimentere
    aruco_perimeter=cv2.arcLength(corners[0],True)

    #Pixel to cm
    pixel_cm=aruco_perimeter/20

    contours=detector.detect_objects(img)

    #draw object boundaries
    for cnt in contours:

        #Draw polygon 
        cv2.polylines(img, [cnt], True, (255,0,0), 2) 

        #get rectangle
        rect=cv2.minAreaRect(cnt)
        (x,y),(w,h,),angle=rect

        #get object dimensions in cm
        object_width=w/pixel_cm
        object_height=h/pixel_cm
        
        #Display rectangle
        box=cv2.boxPoints(rect)
        box=np.int0(box)

        cv2.circle(img,(int (x),int(y)),5,(0,0,255),-1)
        cv2.polylines(img, [box], True, (255,0,0), 2)
        cv2.putText(img, "Width {}cm".format(round(object_width,1)),(int(x+5),int(y-15)), cv2.FONT_HERSHEY_TRIPLEX, 0.5, (100,255,51))
        cv2.putText(img, "Height {}cm".format(round(object_height,1)),(int(x+5),int(y+5)), cv2.FONT_HERSHEY_TRIPLEX, 0.5, (100,255,51))

        

    cv2.imshow("Image", img)
    key=cv2.waitKey(1)
    if key==27:
        break

cap.release()
cv2.destroyAllWindows()