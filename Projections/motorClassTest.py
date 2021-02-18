from multipleMotorClass import StepperMotors

VOLT = [2] # tester to see if pi pinout can handle lvl converting using GPIO pins
PUL = [17]  # Stepper Drive Pulses
DIR = [27]  # Controller Direction Bit (High for Controller default / LOW to Force a Direction Change).
OPTO = [22]  # Controller Enable Bit (High to Enable / LOW to Disable).

stepper1 = StepperMotors(VOLT,PUL,DIR,OPTO,400,0,1)

stepper1.driveRotMotor(1,1)