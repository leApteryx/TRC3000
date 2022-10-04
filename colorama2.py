import cv2
import numpy as np
np.set_printoptions(threshold=np.inf)

#Load cam_image
cam = cv2.VideoCapture(0)

cv2.namedWindow("test")

img_counter = 0

while True:
    ret, frame = cam.read()
    if not ret:
        print("failed to grab frame")
        break
    cv2.imshow("test", frame)

    k = cv2.waitKey(1)
    if k%256 == 27:
        # ESC pressed
        print("Escape hit, closing...")
        break
    elif k%256 == 32:
        # SPACE pressed
        img_name = "opencv_frame_{}.png".format(img_counter)
        cv2.imwrite(img_name, frame)
        print("{} written!".format(img_name))
        img_counter += 1

cam.release()

cv2.destroyAllWindows()

img = cv2.imread('opencv_frame_0.png')

#define kernel size  
kernel = np.ones((7,7),np.uint8)

# convert to hsv colorspace 
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
# lower bound and upper bound for Blue color 
lower_bound = np.array([101, 50, 38])     
upper_bound = np.array([110, 255, 255])

# find the colors within the boundaries
mask = cv2.inRange(hsv, lower_bound, upper_bound)

# Remove unnecessary noise from mask
mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

# Segment only the detected region
segmented_img = cv2.bitwise_and(img, img, mask=mask)
# Find contours from the mask
contours, hierarchy = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
# Draw contour on original image
output = cv2.drawContours(img, contours, -1, (0, 0, 255), 3)

#Load cam_image
cam = cv2.VideoCapture(0)

cv2.namedWindow("test")

img_counter = 0

while True:
    ret, frame = cam.read()
    if not ret:
        print("failed to grab frame")
        break
    cv2.imshow("test", frame)

    k = cv2.waitKey(1)
    if k%256 == 27:
        # ESC pressed
        print("Escape hit, closing...")
        break
    elif k%256 == 32:
        # SPACE pressed
        img_name = "opencv_frame_{}.png".format(img_counter)
        cv2.imwrite(img_name, frame)
        print("{} written!".format(img_name))
        img_counter += 1

cam.release()

cv2.destroyAllWindows()

img = cv2.imread('opencv_frame_0.png')

#define kernel size  
kernel = np.ones((7,7),np.uint8)

# convert to hsv colorspace 
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
# lower bound and upper bound for Blue color 
lower_bound = np.array([101, 50, 38])     
upper_bound = np.array([110, 255, 255])

# find the colors within the boundaries
mask2 = cv2.inRange(hsv, lower_bound, upper_bound)

# Remove unnecessary noise from mask
mask2 = cv2.morphologyEx(mask2, cv2.MORPH_CLOSE, kernel)
mask2 = cv2.morphologyEx(mask2, cv2.MORPH_OPEN, kernel)
# Segment only the detected region
segmented_img = cv2.bitwise_and(img, img, mask=mask2)
# Find contours from the mask
contours, hierarchy = cv2.findContours(mask2.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Comparing masks for similarity
compare=mask==mask2
true_count= np.count_nonzero(compare)
false_count=np.size(compare)-true_count
if (true_count<false_count):
    print("Color change detected!!")
else:
    print("Color change not detected!!")

cv2.waitKey(0)
cv2.destroyAllWindows()

