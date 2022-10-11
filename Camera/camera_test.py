#!/usr/bin/env python3

from picamera import PiCamera
import keyboard
from PIL import Image #PIL = Python Imaging Library

camera = PiCamera()
camera.resolution = (1024, 768)
camera.start_preview()
while True:
    if keyboard.read_key() == "p":
        camera.capture("test.jpg")
        im = Image.open("test.jpg")
        print("Image saved! Opening image...")
        im.show()
        break
