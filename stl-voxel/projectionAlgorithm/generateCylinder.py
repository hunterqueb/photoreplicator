import time
import math

import pygame
from libraries.wavelengthToRGB.wavelengthToRGB import wavelengthToRGB

def generateCylinder():
    gamma = 1
    #colors in wavelengths in nanometers
    backgroundWavelength = 580 #yellow
    objectWavelength = 460 #blue

    pygame.init()
    screen = pygame.display.set_mode([1920, 1080], 0, 32) #display 0 is the main screen, display 1 is the secondary monitor

    done = False

    while not done:
        for event in pygame.event.get():  # User did something
            if event.type == pygame.QUIT:  # If user clicked close
                done = True  # Flag that we are done so we exit this loop
            elif pygame.mouse.get_pressed()[2]: #on riight click, exit the window
                done = True
            else: #inner loop to generate images
                screen.fill(wavelengthToRGB(backgroundWavelength,gamma)) #fill the screen with a color that will not harden resin
        
        
        
        
        pygame.display.flip()


generateCylinder()


