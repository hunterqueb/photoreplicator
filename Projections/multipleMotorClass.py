import RPi.GPIO as GPIO
from time import sleep
import os
import threading

# designed to be called as a thread
no_input = True

def signal_user_input():
    global no_input
    print("hit enter to stop things")
    i = input()
    no_input = False
    # thread exits here


class StepperMotors:
    def __init__(self,VOLT,PUL,DIR,OPTO,PULSES_PER_REV,LEAD,MOTOR_COUNT):
    # takes the input on construction the pin to control voltage, pin to pulse, pin to change direction, pin to enable opto
    #   -these pins are enabled referred as the GPIO pin references
    # a boolean value to choose the whether the motor is apart of the lead screw array or whether is it the direct drive motor
    # and the GPIO object
    # all variables are in the form of arrays with the last, MOTOR_COUNT, being an integer
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)

        if (len(VOLT) != MOTOR_COUNT | len(PUL) != MOTOR_COUNT | len(DIR) != MOTOR_COUNT | len(OPTO) != MOTOR_COUNT | len(PULSES_PER_REV) != MOTOR_COUNT | len(LEAD) != 3):
            raise Exception()

        self.VOLT = VOLT
        self.PUL = PUL
        self.DIR = DIR
        self.OPTO = OPTO
        self.LEAD = LEAD
        self.PULSES_PER_REV = PULSES_PER_REV
        self.LEAD_DISTANCE = 8 # in mm
        self.STEPS_PER_REV = 200 # same for both nema 11 and nema 17
        self.currentDirection = [GPIO.LOW, GPIO.LOW, GPIO.LOW]
        self.MOTOR_COUNT = int(MOTOR_COUNT)

        for i in range(MOTOR_COUNT):
            GPIO.setup(self.PUL[i], GPIO.OUT)
            GPIO.setup(self.OPTO[i], GPIO.OUT)
            GPIO.output(self.OPTO[i], GPIO.HIGH)

            GPIO.setup(self.VOLT[i], GPIO.OUT)
            GPIO.output(self.VOLT[i], GPIO.HIGH)

            GPIO.setup(self.DIR[i], GPIO.OUT)
            self.currentDirection[i] = GPIO.LOW
            GPIO.output(self.DIR[i], self.currentDirection[i])

            self.motorStep[i] = 0

    def driveRotMotor(self, REVS, TRAVEL_TIME):
        t = threading.Thread(target=signal_user_input)
        t.start()
        self.PULSES_PER_SEC[0] = 2 * self.PULSES_PER_REV[0] * REVS / TRAVEL_TIME
        self.PULSE_DELAY[0] = 0.5 * 1 / self.PULSES_PER_SEC[0]

        while no_input:
            GPIO.output(self.PUL[0], GPIO.HIGH)
            sleep(self.PULSE_DELAY[0])
            GPIO.output(self.PUL[0], GPIO.LOW)
            sleep(self.PULSE_DELAY[0])

    def driveMotors(self, REVS, LEAD_SCREW_TRAVEL_DISTANCE, TRAVEL_TIME):
        self.PULSES_PER_SEC[0] = 2 * self.PULSES_PER_REV[0] * REVS / TRAVEL_TIME
        self.PULSE_DELAY[0] = 0.5 * 1 / self.PULSES_PER_SEC[0]

        for i in range(MOTOR_COUNT-1):
            self.PULSES_PER_SEC[i+1] = 2 * self.PULSES_PER_REV[i+1]  * LEAD_SCREW_TRAVEL_DISTANCE / (self.LEAD_DISTANCE * TRAVEL_TIME)
            self.PULSE_DELAY[i+1] = 0.5 * 1 / self.PULSES_PER_SEC[i+1]

        motorStepTarget = [REVS, (self.LEAD_DISTANCE * TRAVEL_TIME),(self.LEAD_DISTANCE * TRAVEL_TIME)]

        for i in range(MOTOR_COUNT):
            motorStepTarget[i] = 200 * motorStepTarget[i]
            if self.currentDirection[i] == 1:
                motorStepTarget[i] = self.motorStep[i] - motorStepTarget[i]

        while self.motorStep[2] < motorStepTarget[2]:
            GPIO.output(self.PUL[0], GPIO.HIGH)
            sleep(self.PULSE_DELAY[0])
            GPIO.output(self.PUL[0], GPIO.LOW)
            sleep(self.PULSE_DELAY[0])
            if self.motorStep[1] < motorStepTarget[1]:
                GPIO.output(self.PUL[1], GPIO.HIGH)
                sleep(self.PULSE_DELAY[1])
                GPIO.output(self.PUL[1], GPIO.LOW)
                sleep(self.PULSE_DELAY[1])
                self.motorStep[1] += 1

            if self.motorStep[2] < motorStepTarget[2]:
                GPIO.output(self.PUL[2], GPIO.HIGH)
                sleep(self.PULSE_DELAY[2])
                GPIO.output(self.PUL[2], GPIO.LOW)
                sleep(self.PULSE_DELAY[2])
                self.motorStep[2] += 1

    def changeLeadDirections(self):
        for i in range(2):
            if self.currentDirection[i+1] == GPIO.LOW:
                self.currentDirection[i+1] = GPIO.HIGH
                GPIO.output(self.DIR[i+1], self.currentDirection[i+1])
            else:
                self.currentDirection[i+1] = GPIO.LOW
                GPIO.output(self.DIR[i+1], self.currentDirection[i+1])
