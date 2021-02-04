import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

PUL = 12 # needs to be on a pwn pin - pwn pins are 12, 32, 33, 35 
DIR = 11

# OPTO and ENA pins are not needed for this application
# 

GPIO.setup(DIR, GPIO.out)
pi_pwm = GPIO.PWM(PUL, 133333)
pi_pwm.start(0)

SPR = 400 # value dependent on the switches on the outside of the driver

pi_pwm.ChangeDutyCycle(50) #half power - this value has a range of 0 to 100 to determine the speed of the motor
time.sleep(5)

GPIO.cleanup()
