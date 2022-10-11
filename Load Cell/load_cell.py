#! /usr/bin/python2

import time
import sys
import math

EMULATE_HX711=False

referenceUnit = 1

if not EMULATE_HX711:
    import RPi.GPIO as GPIO
    from hx711 import HX711
else:
    from emulated_hx711 import HX711

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
