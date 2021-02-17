import RPi.GPIO as GPIO
from time import sleep
from libraries.stepperMotor.StepperMotorClass import StepperMotor

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
GPIO.cleanup()


VOLT = 2 # tester to see if pi pinout can handle lvl converting using GPIO pins
PUL = 17  # Stepper Drive Pulses
DIR = 27  # Controller Direction Bit (High for Controller default / LOW to Force a Direction Change).
OPTO = 22  # Controller Enable Bit (High to Enable / LOW to Disable).

stepper1 = StepperMotor(VOLT,PUL,DIR,OPTO,400,0)

while True:
    stepper1.driveMotorVel(1)
    sleep(1)
#    stepper1.changeDirection()
#    stepper1.driveMotorVel(2)
#    sleep(1)
#    stepper1.changeDirection()
#    stepper1.driveMotorVel(1)
    
GPIO.cleanup()
