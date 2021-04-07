import pyglet
from pyglet.window import key
from pyglet import shapes

import sys
from libraries.wavelengthToRGB.wavelengthToRGB import wavelengthToRGB
from libraries.vertexClass.vertexClass import pygletVertex

# TODO
# add cup -- u shaped object
# fix pawn shape
# add hourglass shape
# look into import shapes/sillouettes into pyglet

# prints 30 pixels/mm
# accuracy of 33 microns -

try:
    objectToProject = sys.argv[1]
except:
    objectToProject = "rectangle"
    print('object not specified, defaulting to rectangle')

# to be done for this project
# need to get find how to update picture of foreground object with refresh rate of monitor
# need to write a function to flip the geometry of whatever is being displayed
# need to write a funciton that generates object picturewith depth
# figure out the relative imports

# get the displays and screen information
displays = pyglet.canvas.get_display()
screens = displays.get_screens()

# instance the window object for each display
window1 = pyglet.window.Window(
    1920, 1080, fullscreen=False, screen=screens[0], visible=True)
#window2 = pyglet.window.Window(
#    fullscreen=True, screen=screens[0], visible=False)


# create a batch of shapes the program draws
resinPreheat = pyglet.graphics.Batch()
deactivateResin = pyglet.graphics.Batch()
backgroundBatch = pyglet.graphics.Batch()

batch = pyglet.graphics.Batch()
# initialize the wavelengths for colors to be used by the wavelength to RGB function
gamma = 1
#colors in wavelengths in nanometers
backgroundWavelength = 580  # yellow
foregroundWavelength = 405  # purple
visibleForegroundWavelenth = 680  # red

colorToDraw = visibleForegroundWavelenth

# create variables that store the value of where the shapes should be drawn
background = shapes.Rectangle(
    0, 0, screens[0].width, screens[0].height, color=wavelengthToRGB(backgroundWavelength, gamma), batch=backgroundBatch)

purpleBackground = shapes.Rectangle(0, 0, screens[0].width, screens[0].height, color=wavelengthToRGB(
    foregroundWavelength, gamma), batch=resinPreheat)

yellowBackground = shapes.Rectangle(0, 0, screens[0].width, screens[0].height, color=wavelengthToRGB(
    backgroundWavelength, gamma), batch=deactivateResin)

foregroundObjectShapes = [None, None, None]

if objectToProject == "rectangle":
    objectDrawn = pygletVertex(
        batch, 4, [100, 600, 600, 600, 600, 100, 100, 100])
    global vertexList
    vertexList = objectDrawn.initialDraw(batch)
    vertexList.delete()
    vertexList = objectDrawn.movePolygon(batch, "right", 700)

draw = 0


# create event handlers that update with drawing the batch, im not sure how often this occurs
@window1.event
def on_draw():
    window1.clear()
    drawBatch(draw)


#@window2.event
#def on_draw():
#    window2.clear()
#    label.draw()

@window1.event
def on_key_press(symbol, modifiers):
    global draw
    global vertexList
    if symbol == key.ENTER or symbol == key.ESCAPE:
        pyglet.app.exit()
    if symbol == key._1:
        colorToDraw = visibleForegroundWavelenth
        vertexList.delete()
        vertexList = objectDrawn.changeColor(batch, wavelengthToRGB(colorToDraw, gamma))
    if symbol == key._2:
        colorToDraw = foregroundWavelength
        vertexList.delete()
        vertexList = objectDrawn.changeColor(batch, wavelengthToRGB(colorToDraw, gamma))
    if symbol == key.A:
        draw = 0
    if symbol == key.S:
        draw = 1
    if symbol == key.D:
        draw = 2
    if symbol == key.LEFT:
        vertexList.delete()
        vertexList = objectDrawn.movePolygon(batch, "left", 10)
    if symbol == key.RIGHT:

        vertexList.delete()
        vertexList = objectDrawn.movePolygon(batch, "right", 10)

    if symbol == key.UP:

        vertexList.delete()
        vertexList = objectDrawn.movePolygon(batch, "up", 10)

    if symbol == key.DOWN:
        vertexList.delete()
        vertexList = objectDrawn.movePolygon(batch, "down", 10)


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

# run the app
pyglet.app.run()
