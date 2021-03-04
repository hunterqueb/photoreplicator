from libraries.multipleMotorClass.multipleMotorClass import StepperMotors
import sys

VOLT = [2,21,20] # tester to see if pi pinout can handle lvl converting using GPIO pins
PUL = [17,26,16]  # Stepper Drive Pulses
DIR = [27,19,13]  # Controller Direction Bit (High for Controller default / LOW to Force a Direction Change).
OPTO = [22,6,12]  # Controller Enable Bit (High to Enable / LOW to Disable).

PULSES_PER_REV_MOTOR1 = 800
PULSES_PER_REV_MOTOR2 = 400
PULSES_PER_REV_MOTOR3 = 400

PULSES_PER_REV = [PULSES_PER_REV_MOTOR1,PULSES_PER_REV_MOTOR2,PULSES_PER_REV_MOTOR3]

stepper1 = StepperMotors(VOLT,PUL,DIR,OPTO,PULSES_PER_REV,0,1)
try:
    revs1 = sys.argv[1]

    revs = float(revs1)

except:
    revs = 0.1666667
    print("defaulting to 0.166 revs/sec")
stepper1.driveRotMotor(revs,1)
