from time import sleep
import os


class StepperMotors:
    def __init__(self, VOLT, PUL, DIR, OPTO, PULSES_PER_REV, LEAD, MOTOR_COUNT):
        # takes the input on construction the pin to control voltage, pin to pulse, pin to change direction, pin to enable opto
        #   -these pins are enabled referred as the GPIO pin references
        # a boolean value to choose the whether the motor is apart of the lead screw array or whether is it the direct drive motor
        # and the GPIO object
        # all variables are in the form of arrays with the last, MOTOR_COUNT, being an integer

        # this is a tester class used for unit testing outside of pi hardware

        self.VOLT = VOLT
        self.PUL = PUL
        self.DIR = DIR
        self.OPTO = OPTO
        self.LEAD = LEAD
        self.PULSES_PER_REV = PULSES_PER_REV
        self.LEAD_DISTANCE = 8  # in mm
        self.STEPS_PER_REV = 200  # same for both nema 11 and nema 17
        self.MOTOR_COUNT = int(MOTOR_COUNT)
        self.motorStep = [0, 0, 0]
        self.PULSES_PER_SEC = [0, 0, 0]
        self.PULSE_DELAY = [0, 0, 0]
        self.currentDirection = [0, 1, 1]
        
        for i in range(MOTOR_COUNT):
            self.motorStep[i] = 0


    def driveRotMotor(self, REVS, TRAVEL_TIME):
        self.PULSES_PER_SEC[0] = 2 * self.PULSES_PER_REV[0] * REVS / TRAVEL_TIME
        self.PULSE_DELAY[0] =  1 / self.PULSES_PER_SEC[0]

        print("Pulse High") # this is where we would pulse the actual GPIO pin
        sleep(self.PULSE_DELAY[0])
        print("Pulse Low")
        sleep(self.PULSE_DELAY[0])
        print("end")
        # if self.currentDirection[0] == 0:
        #     motorStep[0] += 1
        # else:
        #     motorStep[0] -= 1


    def driveMotors(self, REVS, LEAD_SCREW_TRAVEL_DISTANCE, TRAVEL_TIME):
        self.PULSES_PER_SEC[0] = 2 * \
            self.PULSES_PER_REV[0] * REVS / TRAVEL_TIME
        self.PULSE_DELAY[0] = 0.5 * 1 / self.PULSES_PER_SEC[0]

        for i in range(MOTOR_COUNT-1):
            self.PULSES_PER_SEC[i+1] = 2 * self.PULSES_PER_REV[i+1] * \
                LEAD_SCREW_TRAVEL_DISTANCE / (self.LEAD_DISTANCE * TRAVEL_TIME)
            self.PULSE_DELAY[i+1] = 1 / self.PULSES_PER_SEC[i+1]

        motorStepTarget = [
            REVS, (self.LEAD_DISTANCE * TRAVEL_TIME), (self.LEAD_DISTANCE * TRAVEL_TIME)]

        for i in range(MOTOR_COUNT):
            motorStepTarget[i] = 200 * motorStepTarget[i]
            if self.currentDirection[i] == 1:
                motorStepTarget[i] = self.motorStep[i] - motorStepTarget[i]

        while self.motorStep[2] < motorStepTarget[2]:
            
            if self.motorStep[1] < motorStepTarget[1]:
                
                self.motorStep[1] += 1

            if self.motorStep[2] < motorStepTarget[2]:
                
                self.motorStep[2] += 1

    def changeLeadDirections(self, DIRECTION):
        for i in range(2):
            if DIRECTION == "UP":
                pass
            elif DIRECTION == "DOWN":
                pass
            else:
                raise Exception()
