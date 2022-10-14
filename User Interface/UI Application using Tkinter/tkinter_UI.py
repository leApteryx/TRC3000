# TRC3000 Project
# Team 212
# Project Title: Anaerobic Digester Sample Tester
# Date of Submission: 2022-10-14

import tkinter as tk
from tkinter import ttk
from tkinter import *
import tkinter.font as font
from tkinter.messagebox import showerror
import RPi.GPIO as GPIO  # import GPIO
from hx711 import HX711  # import the class HX711
import time
import math
import sys
import smbus2
from time import sleep
import cv2
import numpy as np
from PIL import Image, ImageTk # PIL = Python Imaging Library


#------------------------------------------ System Setup ---------------------------------------------#

# IMU Constants
PWR_MGMT_1 = 0x6B
SMPLRT_DIV = 0x19
CONFIG = 0x1A
GYRO_CONFIG = 0x1B
INT_ENABLE = 0x38
ACCEL_XOUT_H = 0x3B
ACCEL_YOUT_H = 0x3D
ACCEL_ZOUT_H = 0x3F
GYRO_XOUT_H = 0x43
GYRO_YOUT_H = 0x45
GYRO_ZOUT_H = 0x47
bus = smbus2.SMBus(1)
Device_Address = 0x68

# Counts the number of captured images
current_frame = 1

# GPIO Setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(16, GPIO.OUT) # GPIO.BOARD = 36 (load cell)
GPIO.setup(21, GPIO.OUT) # GPIO.BOARD = 40 (servo)


#------------------------------------------ Functions ---------------------------------------------#

# Function: To reset the display in the app
def setup(function):
    Output.delete("1.0", END) # clear existing output
    Output.insert(END, "Now running: " + function)
    Output.update()
    
# Function: To turn off all the relays    
def cleanup():
    GPIO.output(16, GPIO.HIGH) # GPIO.BOARD = 36 (load cell)
    GPIO.output(21, GPIO.HIGH) # BOARD no. = 40 (servo)
    Output.insert(END, "\nGoodbye!")
    Output.update()

# Function: To close the user interface app
def on_closing():
    GPIO.cleanup()
    print("UI closed!")
    root.destroy()

# Function: To take a single measurement from the load cell
def load_cell():
    setup(load_cell.__name__)
    
    # turn on load cell relay
    GPIO.output(16, GPIO.LOW) # GPIO.BOARD = 36

    # tare load cell
    hx = HX711(5, 6)
    hx.set_reading_format("MSB", "MSB")
    hx.reset()
    hx.tare()
    
    Output.insert(END, "\nLoad cell tared! Add item now:")
    Output.update()

    # read load cell
    load = 0
    while not load:
        val = hx.get_weight(5)
        load = math.trunc(val*0.0044)
        Output.insert(END, "\n" + str(load))
        Output.update()

        hx.power_down()
        hx.power_up()
        time.sleep(0.1)
    
    # clean up
    cleanup()

# Function: To reset the servo's position
def servo():
    setup("resetting the servo's position")
    
    # Turn on servo relay
    GPIO.output(21, GPIO.LOW) # GPIO.BOARD = 40

    # Set pin 11 as an output, and set servo1 as pin 11 as PWM
    GPIO.setup(17, GPIO.OUT) # BOARD no. = 11
    servo1 = GPIO.PWM(17, 50) # pin 17, 50Hz pulse

    #start PWM running, but with value of 0 (pulse off)
    servo1.start(0)
    Output.insert(END, "\nWaiting for 2 seconds")
    Output.update()
    time.sleep(2)

    #Let's move the servo!
    Output.insert(END, "\nRotating 180 degrees in 4 steps")
    Output.update()

    # Define variable duty
    duty = 2

    # Loop for duty values from 2 to 12 (0 to 180 degrees)
    while duty <= 11:
        servo1.ChangeDutyCycle(duty)
        time.sleep(1)
        duty = duty + 3

    # Wait a couple of seconds
    time.sleep(2)

    # Turn back to 90 degrees
    Output.insert(END, "\nTurning back to 90 degrees for 2 seconds")
    Output.update()
    # print ("Turning back to 90 degrees for 2 seconds")
    servo1.ChangeDutyCycle(7)
    time.sleep(2)

    #turn back to 0 degrees
    Output.insert(END, "\nTurning back to 0 degrees")
    Output.update()
    # print ("Turning back to 0 degrees")
    servo1.ChangeDutyCycle(2)
    time.sleep(0.5)
    servo1.ChangeDutyCycle(0)

    #Clean things up at the end
    servo1.stop()
    GPIO.output(21, GPIO.HIGH) # BOARD no. = 40
    cleanup()

# Subfunction: To declare addresses from the IMU chip
def MPU_Init():
    bus.write_byte_data(Device_Address, SMPLRT_DIV, 7)
    bus.write_byte_data(Device_Address, PWR_MGMT_1, 1)
    bus.write_byte_data(Device_Address, CONFIG, 0)
    bus.write_byte_data (Device_Address, GYRO_CONFIG, 24)
    bus.write_byte_data(Device_Address, INT_ENABLE, 1)

# Subfunction: To read the raw data from the IMU chip
def read_raw_data(addr):
    high = bus.read_byte_data(Device_Address, addr)
    low = bus.read_byte_data(Device_Address, addr + 1)
    value = ((high << 8)| low)
    if (value > 32768):
        value = value - 65536
    return value

# Function: To take a single measurement from the IMU
def imu():
    setup("IMU")
     
    MPU_Init()
    acc_x = read_raw_data(ACCEL_XOUT_H)
    acc_y = read_raw_data(ACCEL_YOUT_H)
    acc_z = read_raw_data(ACCEL_ZOUT_H)
 
    gyro_x = read_raw_data(GYRO_XOUT_H)
    gyro_y = read_raw_data(GYRO_YOUT_H)
    gyro_z = read_raw_data(GYRO_ZOUT_H)
 
    Ax = round(acc_x/15000, 2)
    Ay = round(acc_y/15000, 2)
    Az = round(acc_z/15000, 2)
 
    Gx = round(gyro_x/131, 2)
    Gy = round(gyro_y/131, 2)
    Gz = round(gyro_z/131, 2)
 
    Output.insert(END, "\nGyrocope (degrees/s): \nGx = " + str(Gx) + " | Gy = " + str(Gy) + " | Gz = " + str(Gz))
    Output.insert(END, "\nAcceleration (g): \nAx = " + str(Ax) + " | Ay = " + str(Ay) + " | Az = " + str(Az))
    Output.update()

# Function: To capture an image using the camera
def take_image():
    setup("take image")
    global current_frame
    cap = cv2.VideoCapture(0)

    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)
    name = 'image' + str(current_frame) + '.jpg'
    cv2.imwrite(name, frame)
    im = Image.open(name)
    im.show()
    current_frame += 1

    cap.release()
    cv2.destroyAllWindows()
    
# Function: To capture 3 different images from 3 different angles using the camera and the servo
def take_three_images():
    setup("take 3 images from 3 different angles")
    
    global current_frame
    
    # Turn on servo relay
    GPIO.output(21, GPIO.LOW) # GPIO.BOARD = 40

    # Set pin 11 as an output, and set servo1 as pin 11 as PWM
    GPIO.setup(17, GPIO.OUT) # BOARD no. = 11
    servo1 = GPIO.PWM(17, 50) # pin 17, 50Hz pulse

    #start PWM running, but with value of 0 (pulse off)
    servo1.start(0)
    
    servo1.ChangeDutyCycle(2)
    take_image()
    servo1.ChangeDutyCycle(7)
    take_image()
    servo1.ChangeDutyCycle(12)
    take_image()

# Function: To stream the camera
def stream_camera():
    setup("stream camera")
    Output.insert(END, "\nCamera closing in 5s...")
    Output.update()
    cap = cv2.VideoCapture(0)
    
    while True:
        ret, frame = cap.read()
        frame = cv2.flip(frame, 1)
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
    cap.release()
    cv2.destroyAllWindows()


#------------------------------------------ User Interface ---------------------------------------------#

# Define the root window
root = tk.Tk()

# Acquire the device screen size
width = math.floor(root.winfo_screenwidth())
height = math.floor(root.winfo_screenheight())

# Format the root window
root.title('Anaerobic Digestate Tester')
root.geometry(f"{str(width)}x{str(height)}")
root.resizable(False, False)
root.option_add("*font", "arial 25")
root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
# root.grid_columnconfigure(2, weight=8)

# Create calibration label frame
calib_frame = ttk.LabelFrame(root, text='Calibration Options')
calib_frame.grid(column=0, row=0, padx=10, pady=20, ipadx=20, ipady=20, sticky="se")

# Create operations label frame
ops_frame = ttk.LabelFrame(root, text='Operations')
ops_frame.grid(column=1, row=0, padx=10, pady=20, ipadx=20, ipady=20, sticky="sw")

# Add buttons and their corresponding functions
calib_dict = {"check IMU readings": imu,
              "read load cell": load_cell,
              "reset servo position": servo
              }

ops_dict = {"take image": take_image,
            "take 3 images" : take_three_images,
            "stream camera": stream_camera
            }

for name, function in calib_dict.items():
    tk.Button(calib_frame, width=20, text=name, padx=5, pady=5, command=function).pack()
    
for name, function in ops_dict.items():
    tk.Button(ops_frame, width=20, text=name, padx=5, pady=5, command=function).pack()
    
# Create output label frame
output_frame = ttk.LabelFrame(root, text='Output')
output_frame.grid(column=0, row=1, columnspan=2, padx=20, pady=0, ipadx=20, ipady=20, sticky="n")

# Set output text box
Output = Text(output_frame, height=10, width=50)
Output.pack()

# Launch the app
root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()