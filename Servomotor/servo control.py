import RPi.GPIO as GPIO
import time


def map_range(x, in_min, in_max, out_min, out_max):
  return (x - in_min) * (out_max - out_min) // (in_max - in_min) + out_min

def moveServoForward(duty,myServo,speed):
    mapSpeed = map_range(speed,0,30,30,0)
    while duty <= 12:
        myServo.ChangeDutyCycle(duty)
        time.sleep(mapSpeed)
        duty = duty + 1



if __name__ == "__main__":
    try:
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(11,GPIO.OUT)
        servo1 = GPIO.PWM(11,50)

        print("Initialising and waiting for 2 seconds")
        servo1.start(0)
        time.sleep(2)

        
        duty_cycle = int(input("Enter a position between 2 and 12 inclusive: "))
        speed = int(input ("Enter a speed between 0 and 30 inclusive: "))
        time1 = time.time()
        moveServoForward(duty_cycle,servo1,speed)
        time2 = time.time()
        Execution_time = time2-time1
        print(f'Time taken to move to position: {Execution_time}')
    except KeyboardInterrupt:
        print("Turning back to position 0")
        servo1.ChangeDutyCycle(2)
        time.sleep(0.5)
        servo1.ChangeDutyCycle(0)
        servo1.stop()
        GPIO.cleanup()
        print("Exiting servo-control")