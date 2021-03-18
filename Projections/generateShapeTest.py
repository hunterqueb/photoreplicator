import pyglet
from pyglet.window import key
from pyglet import shapes
import time
import sys
import threading

from libraries.wavelengthToRGB.wavelengthToRGB import wavelengthToRGB
from libraries.vertexClass.vertexClass import pygletVertex
from libraries.multipleMotorClass.multipleMotorClassTest import StepperMotors

# TODO
# fix pawn shape
# add hourglass shape
# look into import shapes/sillouettes into pyglet
# need to write a function to flip the geometry of whatever is being displayed
# figure out the relative imports

# prints 30 pixels/mm
# accuracy of 33 microns
# this is subject to change as a result of changing the focul lengths of the magnifying glasses

# # # PREWINDOW SETUP # # #
global running
running = False
global threadOff
threadOff = False
def runCentralMotor():
    while not threadOff:
        while running:
            # print("Running")
            stepper1.driveRotMotor(revs,1)
    return
            
    # thread exits here

# taking the input from the user, we need to know what shape to draw. if no input is added, then we default to a rectangle
try:
    objectToProject = sys.argv[1]
except:
    objectToProject = "rectangle"
    print('object not specified, defaulting to rectangle')



# get the displays and screen information
displays = pyglet.canvas.get_display()
screens = displays.get_screens()

# instance the window object for each display
window1 = pyglet.window.Window(1920, 1080, fullscreen=False, screen=screens[0], visible=False)
# window2 = pyglet.window.Window(1920, 1080, fullscreen=False, screen=screens[1], visible=False)

# # # PREDRAWING SETUP # # #

# create a batch of shapes the program draws - this is how pyglet draws. you load things you want to project into a batch, then when drawing the batch it draws all shapes at once
resinPreheat = pyglet.graphics.Batch()
deactivateResin = pyglet.graphics.Batch()
backgroundBatch = pyglet.graphics.Batch()

# this batch is a seperate one for drawing the foreground object
batch = pyglet.graphics.Batch()

# initialize the wavelengths for colors to be used by the wavelength to RGB function
gamma = 1
#colors in wavelengths in nanometers
backgroundWavelength = 580  # yellow
foregroundWavelength = 405  # purple
visibleForegroundWavelenth = 680 # red
# initialize all shapes that are first drawn to the visible foreground wavelength to help with lining up the image in the buid volume
colorToDraw = visibleForegroundWavelenth

# create variables that store the value of where the shapes should be drawn -- this starts with the backgrounds
# 3 backgrounds are generated, one for normal use as the standard background, one that is for preactivating the resin, and one for having no image show up 
background = shapes.Rectangle(
    0, 0, screens[0].width, screens[0].height, color=wavelengthToRGB(backgroundWavelength, gamma), batch=backgroundBatch)

purpleBackground = shapes.Rectangle(0, 0, screens[0].width, screens[0].height, color=wavelengthToRGB(
    foregroundWavelength, gamma), batch=resinPreheat)

yellowBackground = shapes.Rectangle(0, 0, screens[0].width, screens[0].height, color=wavelengthToRGB(
    backgroundWavelength, gamma), batch=deactivateResin)


# as well, some of the primitive shapes use pyglets framework, and we can draw more complex shapes using a variety of polygons. here, we initilze the 
# foregroundObjectShapes array with the number of polygons
NUM_OF_POLYGONS = 5
foregroundObjectShapes = [None]*NUM_OF_POLYGONS

# # # DRAWING THE OBEJECT TO PROJECT # # #

# when drawing the object either the pyglet framework is used which is simpler to use and read, but cannot draw complex shapes very well
if objectToProject == "rectangle":
    rectangleWidth = 500
    rectangleHeight = 120
    foregroundObjectShapes[0] = shapes.Rectangle(
        width=rectangleWidth, height=rectangleHeight, x=screens[0].width//2 - rectangleWidth, y=screens[0].height//2 - rectangleHeight, color=wavelengthToRGB(colorToDraw, gamma), batch=batch)
elif objectToProject == "circle":
    foregroundObjectShapes[0] = shapes.Circle(x=screens[0].width//2, y=screens[0].height//2, radius=250, color=wavelengthToRGB(colorToDraw, gamma), batch=batch)
elif objectToProject == "pawn":
    # our first primitive complex shape. this draws a psuedo pawn that looks sort of like a cartoon
    rectangleWidth = 200
    rectangleHeight = 600
    foregroundObjectShapes[0] = shapes.Rectangle(
        width=rectangleWidth, height=rectangleHeight/2, x=screens[0].width//2, y=screens[0].height//2 - rectangleHeight, color=wavelengthToRGB(colorToDraw, gamma), batch=batch)
    foregroundObjectShapes[1] = shapes.Circle(
        x=screens[0].width//2 + rectangleWidth//2, y=screens[0].height//3, radius=250, color=wavelengthToRGB(colorToDraw, gamma), batch=batch)
    foregroundObjectShapes[2] = shapes.Rectangle(
        width=rectangleHeight, height=rectangleWidth/2, x=screens[0].width//2 - rectangleWidth, y=screens[0].height//2 - rectangleHeight, color=wavelengthToRGB(colorToDraw, gamma), batch=batch)
elif objectToProject == "polygonTest":
    rectangleWidth = int(300*1.2)
    rectangleHeight = int(500*1.2)
    startPos = 100
    # in order to draw a polygon, you need to follow this format
    # first define the objectDrawn object using the class, pass in the batch, vertex count, and vertices locations
    # the idea is we can find test however we want.
    polygon = [startPos, startPos+rectangleHeight, 
               startPos + rectangleWidth, startPos+rectangleHeight, 
               startPos + rectangleWidth, startPos, 
               startPos, startPos]

    objectDrawn = pygletVertex(batch, polygon, colorToDraw)
    # now draw the initial batches
    vertexList = objectDrawn.initialDraw(batch)
    
    # when you want to move the object to the right, you have to follow this general format
    # you must first delete the vertexList
    vertexList.delete()
    # then you call the method to redraw the polygon
    vertexList = objectDrawn.movePolygon(batch, "right", 700)
elif objectToProject == "classTest":
    polygon = [screens[0].width/2 - 600, 0,
                screens[0].width/2 - 600, screens[0].height,
                screens[0].width/2 - 600 + 120, screens[0].height,
                screens[0].width/2 - 600 + 120, 120,
                screens[0].width/2, 120,
                screens[0].width/2 + 600 - 120, 120,
                screens[0].width/2 + 600 - 120, screens[0].height,
                screens[0].width/2 + 600, screens[0].height,
                screens[0].width/2 + 600, 0]
    for i in range(len(polygon)):
        polygon[i] = int(polygon[i])

    objectDrawn = pygletVertex(batch, polygon, colorToDraw)
    vertexList = objectDrawn.initialDraw(batch)
    vertexList.delete()
    vertexList = objectDrawn.scalePolygon(batch,0.85)
    
elif objectToProject == "cup":
    rectangleWidth = 120
    rectangleHeight = 500

    foregroundObjectShapes[0] = shapes.Rectangle(
        width=rectangleWidth, height=rectangleHeight, x=screens[0].width//2-500, y=screens[0].height//2-400, color=wavelengthToRGB(colorToDraw, gamma), batch=batch)
    foregroundObjectShapes[1] = shapes.Rectangle(
        width=rectangleHeight, height=rectangleWidth, x=screens[0].width//2-500, y=screens[0].height//2-400, color=wavelengthToRGB(colorToDraw, gamma), batch=batch)
    foregroundObjectShapes[2] = shapes.Rectangle(
        width=rectangleWidth, height=rectangleHeight, x=screens[0].width//2, y=screens[0].height//2-400, color=wavelengthToRGB(colorToDraw, gamma), batch=batch)

# this draw variable is used to tell the window what batch we want to draw. in this case, 0 indicates that we want the foreground object to be drawn immedietely
draw = 0
startTime = 0
nextColorToDraw = foregroundWavelength

# # # INITALZE MOTOR THINGS # # #

VOLT = [2,21,20] # tester to see if pi pinout can handle lvl converting using GPIO pins
PUL = [17,26,16]  # Stepper Drive Pulses
DIR = [27,19,13]  # Controller Direction Bit (High for Controller default / LOW to Force a Direction Change).
OPTO = [22,6,12]  # Controller Enable Bit (High to Enable / LOW to Disable).

PULSES_PER_REV_MOTOR1 = 800
PULSES_PER_REV_MOTOR2 = 400
PULSES_PER_REV_MOTOR3 = 400

PULSES_PER_REV = [PULSES_PER_REV_MOTOR1,PULSES_PER_REV_MOTOR2,PULSES_PER_REV_MOTOR3]

stepper1 = StepperMotors(VOLT,PUL,DIR,OPTO,PULSES_PER_REV,0,1)

revs = 0.1666667

t = threading.Thread(target=runCentralMotor,daemon = True)
t.start()
# # # EVENT HANDLING # # #

# create event handlers that update with drawing the batch, im not sure how often this occurs
@window1.event
def on_draw():
    window1.clear()
    drawBatch(draw)

#@window2.event
#def on_draw():
#    window2.clear()
#    label.draw()

# another event handler to take in key presses
@window1.event
def on_key_press(symbol, modifiers):
    # these gloab variables are used to modify the shapes drawn or location
    global draw
    global vertexList
    global colorToDraw
    global nextColorToDraw
    global startTime
    global running
    global threadOff
    # exit the window if either key is presses
    if symbol == key.ESCAPE:
        threadOff = False
        # t.join()
        pyglet.app.exit()
    
    # next sequence of keys are 1 and 2 which tell the window to edit the foreground objects color, 1 for red, 2 for violet
    if symbol == key._1:
        colorToDraw = visibleForegroundWavelenth
        # these try and except tries to apply the changes to the either the foreground objects using pyglets framework or my custom class
        try:
            if foregroundObjectShapes[0] == None:
                vertexList.delete()
                vertexList = objectDrawn.changeColor(batch, wavelengthToRGB(colorToDraw, gamma))
            else:
                for i in range(NUM_OF_POLYGONS):
                    foregroundObjectShapes[i].color = wavelengthToRGB(colorToDraw, gamma)
        except:
            pass
    if symbol == key._2:
        colorToDraw = foregroundWavelength
        try:
            if foregroundObjectShapes[0] == None:
                vertexList.delete()
                vertexList = objectDrawn.changeColor(
                    batch, wavelengthToRGB(colorToDraw, gamma))
            else:
                for i in range(NUM_OF_POLYGONS):
                    foregroundObjectShapes[i].color = wavelengthToRGB(colorToDraw, gamma)
        except:
            pass

    # next sequence of keys are Z and X which tell the window to edit the size of the foreground objects
    if symbol == key.Z:
        # increases the size of the objects, however, with the pyglet framework, when complex shapes are used, we can get strange results so it is disabled for those shapes
        # however, it is enabled for the custom vertex class
        try:
            for i in range(len(foregroundObjectShapes)):
                if objectToProject == "rectangle":
                    foregroundObjectShapes[i].width = 1.01*foregroundObjectShapes[i].width
                    foregroundObjectShapes[i].height = 1.01*foregroundObjectShapes[i].height
                elif objectToProject == "circle":
                    foregroundObjectShapes[i].radius = 1.01 * foregroundObjectShapes[i].radius
                else:
                    vertexList.delete()
                    vertexList = objectDrawn.scalePolygon(batch, 1.01)
        except:
            pass
    if symbol == key.X:
        # decreases the size of the objects, see note above about complex shapes
        try:
            for i in range(len(foregroundObjectShapes)):
                if objectToProject == "rectangle":
                    foregroundObjectShapes[i].width = 0.99 * foregroundObjectShapes[i].width
                    foregroundObjectShapes[i].height = 0.99 * foregroundObjectShapes[i].height
                elif objectToProject == "circle":
                    foregroundObjectShapes[i].radius = 0.99 * foregroundObjectShapes[i].radius
                else:
                    vertexList.delete()
                    vertexList = objectDrawn.scalePolygon(batch, 0.99)
        except:
            pass
    # next sequence of keys are A, S and D which tell the window which batch/background to draw
    if symbol == key.A:
        draw = 0 # draw foregroundobject
    if symbol == key.S:
        draw = 1  # draw preheatresin
    if symbol == key.D:
        draw = 2  # draw just yellow background
    
    # next sequence of keys are LEFT,RIGHT,UP,DOWN which move the object around the window
    if symbol == key.LEFT:
        # these try and except tries to apply the changes to the either the foreground objects using pyglets framework or my custom class
        try:
            if foregroundObjectShapes[0] == None:
                vertexList.delete()
                vertexList = objectDrawn.movePolygon(batch, "left", 10)
            else:
                for i in range(NUM_OF_POLYGONS):
                    foregroundObjectShapes[i].x -= 10
        except:
            pass
    if symbol == key.RIGHT:
        try:
            if foregroundObjectShapes[0] == None:
                vertexList.delete()
                vertexList = objectDrawn.movePolygon(batch, "right", 10)
            else:
                for i in range(NUM_OF_POLYGONS):
                    foregroundObjectShapes[i].x += 10
        except:
            pass
    if symbol == key.UP:
        try:
            if foregroundObjectShapes[0] == None:
                vertexList.delete()
                vertexList = objectDrawn.movePolygon(batch, "up", 10)
            else:
                for i in range(NUM_OF_POLYGONS):
                    foregroundObjectShapes[i].y += 10
        except:
            pass
    if symbol == key.DOWN:
        try:
            if foregroundObjectShapes[0] == None:
                vertexList.delete()
                vertexList = objectDrawn.movePolygon(batch, "down", 10)
            else:
                for i in range(NUM_OF_POLYGONS):
                    foregroundObjectShapes[i].y -= 10
        except:
            pass
    if symbol == key.ENTER:
        if nextColorToDraw == visibleForegroundWavelenth:
            try:
                if foregroundObjectShapes[0] == None:
                    vertexList.delete()
                    vertexList = objectDrawn.changeColor(batch, wavelengthToRGB(nextColorToDraw, gamma))
                else:
                    for i in range(NUM_OF_POLYGONS):
                        foregroundObjectShapes[i].color = wavelengthToRGB(nextColorToDraw, gamma)
            except:
                pass
            nextColorToDraw = foregroundWavelength
            if startTime == 0:
                pass
            else:
                endTime = time.time()
                print("Experiment over:")
                print("--- %0.2f minutes and %0.4f seconds---" % (((endTime - startTime)//60),((endTime - startTime)%60)))
                print("--- %0.4f seconds ---" % ((endTime - startTime)))

        else:
            startTime = time.time()
            try:
                if foregroundObjectShapes[0] == None:
                    vertexList.delete()
                    vertexList = objectDrawn.changeColor(batch, wavelengthToRGB(nextColorToDraw, gamma))
                else:
                    for i in range(NUM_OF_POLYGONS):
                        foregroundObjectShapes[i].color = wavelengthToRGB(nextColorToDraw, gamma)
            except:
                pass
            nextColorToDraw = visibleForegroundWavelenth
    if symbol == key.Q:
        running = True
    if symbol == key.W:
        running = False


        
# this function gets the screen to draw and is called whenever the batch gets updated to draw the screen 
def drawBatch(screenToDraw):
    backgroundBatch.draw()
    if screenToDraw == 0:
        batch.draw()
    elif screenToDraw == 1:
        resinPreheat.draw()
    else:
        deactivateResin.draw()

        



# set visible after all initialization
window1.set_visible()
# window2.set_visible()

# # # MAIN WINDOWLOOP # # #

# run the app loop -- here in the future is where you would control the fps and do the manual window flip in a while loop
pyglet.app.run()
