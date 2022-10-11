import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showerror
import RPi.GPIO as GPIO  # import GPIO
from hx711 import HX711  # import the class HX711
import time
import math
import sys
import cv2
import numpy as np 
from picamera.array import PiRGBArray
from picamera import PiCamera 

# functions
def load_cell():
    def cleanAndExit():
        print("Cleaning...")

        if not EMULATE_HX711:
            GPIO.cleanup()
            
        print("Bye!")
        sys.exit()

    hx = HX711(5, 6)
    hx.set_reading_format("MSB", "MSB")
    hx.reset()
    hx.tare()

    print("Tare done! Add weight now...")

    while True:
        try:
            val = hx.get_weight(5)
            print(math.trunc(val*0.0044))

            hx.power_down()
            hx.power_up()
            time.sleep(0.1)

        except (KeyboardInterrupt, SystemExit):
            cleanAndExit()

def servo():
    # Set GPIO numbering mode
    GPIO.setmode(GPIO.BOARD)

    # Set pin 11 as an output, and set servo1 as pin 11 as PWM
    GPIO.setup(11,GPIO.OUT)
    servo1 = GPIO.PWM(11,50) # Note 11 is pin, 50 = 50Hz pulse

    #start PWM running, but with value of 0 (pulse off)
    servo1.start(0)
    print ("Waiting for 2 seconds")
    time.sleep(2)

    #Let's move the servo!
    print ("Rotating 180 degrees in 10 steps")

    # Define variable duty
    duty = 2

    # Loop for duty values from 2 to 12 (0 to 180 degrees)
    while duty <= 12:
        servo1.ChangeDutyCycle(duty)
        time.sleep(1)
        duty = duty + 1

    # Wait a couple of seconds
    time.sleep(2)

    # Turn back to 90 degrees
    print ("Turning back to 90 degrees for 2 seconds")
    servo1.ChangeDutyCycle(7)
    time.sleep(2)

    #turn back to 0 degrees
    print ("Turning back to 0 degrees")
    servo1.ChangeDutyCycle(2)
    time.sleep(0.5)
    servo1.ChangeDutyCycle(0)

    #Clean things up at the end
    servo1.stop()
    GPIO.cleanup()
    print ("Goodbye")


def imu():
    print("imu calibrated!")

def camera():
    cv2.namedWindow("Trackbars")
 
    cv2.createTrackbar("B", "Trackbars", 0, 255, nothing)
    cv2.createTrackbar("G", "Trackbars", 0, 255, nothing)
    cv2.createTrackbar("R", "Trackbars", 0, 255, nothing)

    camera = PiCamera()
    camera.resolution = (640, 480)
    camera.framerate = 30

    rawCapture = PiRGBArray(camera, size=(640, 480))

    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        image = frame.array
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        B = cv2.getTrackbarPos("B", "Trackbars")
        G = cv2.getTrackbarPos("G", "Trackbars")
        R = cv2.getTrackbarPos("R", "Trackbars")

        green = np.uint8([[[B, G, R]]])
        hsvGreen = cv2.cvtColor(green,cv2.COLOR_BGR2HSV)
        lowerLimit = np.uint8([hsvGreen[0][0][0]-10,100,100])
        upperLimit = np.uint8([hsvGreen[0][0][0]+10,255,255])

        mask = cv2.inRange(hsv, lowerLimit, upperLimit)

        result = cv2.bitwise_and(image	, image	, mask=mask)

        cv2.imshow("frame", image)
        cv2.imshow("mask", mask)
        cv2.imshow("result", result)

        key = cv2.waitKey(1)
        rawCapture.truncate(0)
        if key == 27:
            break

    cv2.destroyAllWindows()

def lights():
    print("lights turned on!")

# define root window
root = tk.Tk()

# getting device screen size
width = root.winfo_screenwidth()
height = root.winfo_screenheight()

# format root window
root.title('Anaerobic Digestate Tester')
root.geometry(f"{str(width)}x{str(height)}")
root.resizable(False, False)

# create label frame
lf = ttk.LabelFrame(root, text='Calibration Options')
lf.grid(column=0, row=0, padx=20, pady=20, ipadx=20, ipady=20)

# add calibration buttons
button_dict = {"load cell": load_cell,
               "set servo position": servo,
               "check IMU readings": imu,
               "record image": camera,
               "turn on lights": lights}

for name, function in button_dict.items():
    tk.Button(lf, width=20, text=name, padx=5, pady=5, command=function).pack()

# servo_button = ttk.Button(root, text="Servo", command=servo)

# def fahrenheit_to_celsius(f):
#     """ Convert fahrenheit to celsius
#     """
#     return (f - 32) * 5/9
#
#
# # frame
# frame = ttk.Frame(root)
#
#
# # field options
# options = {'padx': 5, 'pady': 5}
#
# # temperature label
# temperature_label = ttk.Label(frame, text='Fahrenheit')
# temperature_label.grid(column=0, row=0, sticky='W', **options)
#
# # temperature entry
# temperature = tk.StringVar()
# temperature_entry = ttk.Entry(frame, textvariable=temperature)
# temperature_entry.grid(column=1, row=0, **options)
# temperature_entry.focus()
#
# # convert button
#
#
# def convert_button_clicked():
#     """  Handle convert button click event
#     """
#     try:
#         f = float(temperature.get())
#         c = fahrenheit_to_celsius(f)
#         result = f'{f} Fahrenheit = {c:.2f} Celsius'
#         result_label.config(text=result)
#     except ValueError as error:
#         showerror(title='Error', message=error)
#
#
# convert_button = ttk.Button(frame, text='Convert')
# convert_button.grid(column=2, row=0, sticky='W', **options)
# convert_button.configure(command=convert_button_clicked)
#
# # result label
# result_label = ttk.Label(frame)
# result_label.grid(row=1, columnspan=3, **options)
#
# # add padding to the frame and show it
# frame.grid(padx=10, pady=10)


# start the app
root.mainloop()