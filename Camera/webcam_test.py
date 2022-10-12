import cv2
import numpy as np
from PIL import Image #PIL = Python Imaging Library

cap = cv2.VideoCapture(0)

# current_frame = 0
# ret, frame = cap.read()
# frame = cv2.flip(frame, 1)
# name = 'image' + str(current_frame) + '.jpg'
# cv2.imwrite(name, frame)
# im = Image.open(name)
# im.show()


current_frame = 0
while (True):
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)
    name = 'image' + str(current_frame) + '.jpg'
    cv2.imwrite(name, frame)
    im = Image.open(name)
    im.show()
    current_frame += 1
    # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # cv2.imshow('frame', gray)
    # cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
    
cap.release()
cv2.destroyAllWindows()