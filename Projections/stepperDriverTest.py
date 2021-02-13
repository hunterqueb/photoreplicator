import RPi.GPIO as GPIO
import time

# some notes on stepper motors
# the pi outputs a high signal from the GPIO pins as 3.3v and not 5v like the arduino, this means that certain drivers, like the one we are using
# will not work out of the box, we need to connect a 3.3v to 5v circuit to get the required power.
# 
# wire connections
# 
# GPIO 12 to PUL on driver
# GPIO 11 to DIR on driver
#  
# 
# 
# 



GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

PUL = 18  # == RPi 4-Pin #12
DIR = 27  # == RPi 4-Pin #13

# OPTO and ENA pins are not needed for this application

GPIO.setup(DIR, GPIO.OUT)
GPIO.setup(PUL,GPIO.OUT)
pwmPin = GPIO.PWM(PUL, 53333) # 2nd arg. pulse width in hz, minimum for our driver is 7.5 microseconds or 1/(7.5 microsec)
pwmPin.start(0)  # start the pwm at 0 - off

SPR = 400 # value dependent on the switches on the outside of the driver

print("half speed\n")
pwmPin.ChangeDutyCycle(50) # half power - this value has a range of 0 to 100 to determine the speed of the motor
time.sleep(5) 
print("full speed\n")
pwmPin.ChangeDutyCycle(100)
time.sleep(5)
print("quarter speed\n")
pwmPin.ChangeDutyCycle(25)
time.sleep(5)
pwmPin.ChangeDutyCycle(0)
print("done! turning off")



GPIO.cleanup()
