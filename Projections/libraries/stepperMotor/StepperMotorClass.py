import RPi.GPIO as GPIO
from time import sleep
import os

class StepperMotor:
    def __init__(self,VOLT,PUL,DIR,OPTO,PULSES_PER_REV,LEAD):
    # takes the input on construction the pin to control voltage, pin to pulse, pin to change direction, pin to enable opto
    #   -these pins are enabled referred as the GPIO pin references
    # a boolean value to choose the whether the motor is apart of the lead screw array or whether is it the direct drive motor
    # and the GPIO object
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)

        self.VOLT = VOLT
        self.PUL = PUL
        self.DIR = DIR
        self.OPTO = OPTO
        self.LEAD = LEAD
        self.PULSES_PER_REV = PULSES_PER_REV
        self.LEAD_DISTANCE = 8 # in mm
        self.PULSES_PER_SEC = None
        self.PULSE_DELAY = None
        self.STEPS_PER_REV = 200 # same for both nema 11 and nema 17


        GPIO.setup(self.PUL, GPIO.OUT)
        GPIO.setup(self.OPTO, GPIO.OUT)
        GPIO.output(self.OPTO, GPIO.HIGH)

        GPIO.setup(self.VOLT,GPIO.OUT)
        GPIO.output(self.VOLT, GPIO.HIGH)

        GPIO.setup(self.DIR, GPIO.OUT)
        self.currentDirection = GPIO.LOW
        GPIO.output(self.DIR, self.currentDirection)

    def driveMotorVel(self,REV_PER_SEC):
        self.PULSES_PER_SEC = 2 * self.PULSES_PER_REV * REV_PER_SEC
        self.PULSE_DELAY = 0.5 * 1 / self.PULSES_PER_SEC

        for x in range(self.PULSES_PER_SEC): 
            GPIO.output(self.PUL, GPIO.HIGH)
            sleep(self.PULSE_DELAY)
            GPIO.output(self.PUL, GPIO.LOW)
            sleep(self.PULSE_DELAY)

    def driveMotorStep(self,REVS,TIME_OF_ROTATION):
        self.PULSES_PER_SEC = 2 * self.PULSES_PER_REV * REVS / TIME_OF_ROTATION

        self.PULSE_DELAY = 0.5 * 1 / self.PULSES_PER_SEC

        for x in range(self.PULSES_PER_SEC): 
            GPIO.output(self.PUL, GPIO.HIGH)
            sleep(self.PULSE_DELAY)
            GPIO.output(self.PUL, GPIO.LOW)
            sleep(self.PULSE_DELAY)

    def driveMotorLead(self,distance,TIME_OF_ROTATION):
        if self.LEAD == 0:
            print("Error! This motor is not configured as a lead screw motor. As a result, you cannot use this command. Recreate the stepper motor object!")
            return
        
        self.PULSES_PER_SEC = 2 * self.PULSES_PER_REV * distance / (self.LEAD_DISTANCE * TIME_OF_ROTATION)
        self.PULSE_DELAY = 0.5 * 1 / self.PULSES_PER_SEC

        for x in range(self.PULSES_PER_SEC):
            GPIO.output(self.PUL, GPIO.HIGH)
            sleep(self.PULSE_DELAY)
            GPIO.output(self.PUL, GPIO.LOW)
            sleep(self.PULSE_DELAY)

    def changeDirection(self):
        if self.currentDirection == GPIO.LOW:
            self.currentDirection = GPIO.HIGH
        else:
            self.currentDirection = GPIO.LOW

        GPIO.output(self.OPTO, GPIO.LOW)
        sleep(0.001)
        GPIO.output(self.DIR, self.currentDirection)
        GPIO.output(self.OPTO, GPIO.HIGH)

    def changeLead(self):
        if self.LEAD == 0:
            self.LEAD = 1
        else:
            self.LEAD = 0
