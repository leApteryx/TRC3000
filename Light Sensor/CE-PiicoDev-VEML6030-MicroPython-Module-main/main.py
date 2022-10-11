# PiicoDev VEML6030 minimal example code
# This program reads light data from the PiicoDev VEML6030 ambient light sensor
# and displays the result

from PiicoDev_VEML6030 import PiicoDev_VEML6030
import RPi.GPIO as GPIO
import time

# Initialise Sensor
light = PiicoDev_VEML6030()

lightThreshold = 150
LED_PIN = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)
GPIO.output(LED_PIN, GPIO.LOW)
while True:
    # Read and print light data
    lightVal = light.read()
    print("The light intensity is currently " + str(lightVal) + " lux")
    time.sleep(1)
    if lightVal < lightThreshold:
        GPIO.output(LED_PIN, GPIO.HIGH)
        time.sleep(1)
    else:
        GPIO.output(LED_PIN, GPIO.LOW)
        time.sleep(1) 
    time.sleep(1)
    
GPIO.cleanup()
