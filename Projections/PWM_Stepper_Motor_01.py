# Based on: https://www.raspberrypi.org/forums/viewtopic.php?t=242928\.
#
# Software to drive 4 wire stepper motor using a TB6600 Driver
# PRi - RPi 3B
#
# Route 3.3 VDC to the controller "+" input for each: ENA, PUL, and DIR
#
# Connect GPIO pins as shown below) to the "-" input for each: ENA, PUL, and DIR
#
#

# TODO
# - add opto pin set to high
# - find good resource to see how to control the speed of the stepper (arduino's stepper.h could be useful)

from time import sleep
import RPi.GPIO as GPIO
#
# gpio pins are different than the actual pin numbers of the board. when using this, the pins being refered to are the gpio pin references
PUL = 17  # Stepper Drive Pulses
DIR = 27  # Controller Direction Bit (High for Controller default / LOW to Force a Direction Change).
OPTO = 22  # Controller Enable Bit (High to Enable / LOW to Disable).

# NOTE: Leave DIR and ENA disconnected, and the controller WILL drive the motor in Default direction if PUL is applied.

GPIO.setmode(GPIO.BCM)
# GPIO.setmode(GPIO.BOARD) # Do NOT use GPIO.BOARD mode. Here for comparison only. 

GPIO.setup(PUL, GPIO.OUT)
GPIO.setup(DIR, GPIO.OUT)
GPIO.setup(OPTO, GPIO.OUT)

print('PUL = GPIO 17 - RPi 3B-Pin #11')
print('DIR = GPIO 27 - RPi 3B-Pin #13')
print('OPTO = GPIO 22 - RPi 3B-Pin #15')

print('Initialization Completed')

durationFwd = 400 # This is the amount of pusles of the motor spinning. used for forward direction
# this is the number of half pulses to send. if you want to move a whole rev, use the sw4-6 and find the number of pulses per rev and multiply by 2
durationBwd = 400 # This is the amount of pulses of the motor spinning. used for reverse direction

print('Duration Fwd set to ' + str(durationFwd))
print('Duration Bwd set to ' + str(durationBwd))


delay = 0.0000001 # This is actualy a delay between PUL pulses - effectively sets the mtor rotation speed. - need to calculate this

print('Speed set to ' + str(delay))

cycles = 1000 # This is the number of cycles to be run once program is started.
cyclecount = 0 # This is the iteration of cycles to be run once program is started.
print('number of Cycles to Run set to ' + str(cycles))


def forward():
    GPIO.output(OPTO, GPIO.HIGH)
    print('OPTO set to HIGH - Controller Enabled')

    sleep(.5) # pause due to a possible change direction
    GPIO.output(DIR, GPIO.LOW)

    print('DIR set to LOW - Moving Forward at ' + str(delay))
    print('Controller PUL being driven.')
    for x in range(durationFwd): 
        GPIO.output(PUL, GPIO.HIGH)
        sleep(delay)
        GPIO.output(PUL, GPIO.LOW)
        sleep(delay)
    GPIO.output(OPTO, GPIO.LOW)

    print('OPTO set to LOW - Controller Disabled')
    sleep(.5) # pause for possible change direction
    return
#
#
def reverse():
    GPIO.output(OPTO, GPIO.HIGH)
    print('OPTO set to HIGH - Controller Enabled')

    sleep(.5) # pause due to a possible change direction
    GPIO.output(DIR, GPIO.HIGH)

    print('DIR set to LOW - Moving Forward at ' + str(delay))
    print('Controller PUL being driven.')
    for x in range(durationFwd): 
        GPIO.output(PUL, GPIO.HIGH)
        sleep(delay)
        GPIO.output(PUL, GPIO.LOW)
        sleep(delay)
    GPIO.output(OPTO, GPIO.LOW)

    print('OPTO set to LOW - Controller Disabled')
    sleep(.5) # pause for possible change direction
    return

while cyclecount < cycles:
    forward()
    reverse()
    cyclecount = (cyclecount + 1)
    print('Number of cycles completed: ' + str(cyclecount))
    print('Number of cycles remaining: ' + str(cycles - cyclecount))
#
GPIO.cleanup()
print('Cycling Completed')
#
