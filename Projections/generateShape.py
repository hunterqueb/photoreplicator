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
window1 = pyglet.window.Window(1920, 1080, fullscreen=False, screen=screens[0], visible=True)
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
visibleForegroundWavelenth = 680 # red

colorToDraw = visibleForegroundWavelenth

# create variables that store the value of where the shapes should be drawn
background = shapes.Rectangle(
    0, 0, screens[0].width, screens[0].height, color=wavelengthToRGB(backgroundWavelength, gamma), batch=backgroundBatch)

purpleBackground = shapes.Rectangle(0, 0, screens[0].width, screens[0].height, color=wavelengthToRGB(
    foregroundWavelength, gamma), batch=resinPreheat)

yellowBackground = shapes.Rectangle(0, 0, screens[0].width, screens[0].height, color=wavelengthToRGB(
    backgroundWavelength, gamma), batch=deactivateResin)

foregroundObjectShapes = [None,None,None]

if objectToProject == "rectangle":
    rectangleWidth = 200
    rectangleHeight = 600
    foregroundObjectShapes[0] = shapes.Rectangle(
        width=rectangleWidth, height=rectangleHeight, x=screens[0].width//2 - rectangleWidth, y=screens[0].height//2 - rectangleHeight, color=wavelengthToRGB(colorToDraw, gamma), batch=batch)
elif objectToProject == "circle":
    foregroundObjectShapes[0] = shapes.Circle(
        x=screens[0].width//2, y=screens[0].height//2, radius=250, color=wavelengthToRGB(colorToDraw, gamma), batch=batch)
elif objectToProject == "pawn":
    rectangleWidth = 200
    rectangleHeight = 600
    foregroundObjectShapes[0] = shapes.Rectangle(
        width=rectangleWidth, height=rectangleHeight/2, x=screens[0].width//2, y=screens[0].height//2 - rectangleHeight, color=wavelengthToRGB(colorToDraw, gamma), batch=batch)
    foregroundObjectShapes[1] = shapes.Circle(
        x=screens[0].width//2 + rectangleWidth//2, y=screens[0].height//3, radius=250, color=wavelengthToRGB(colorToDraw, gamma), batch=batch)
    foregroundObjectShapes[2] = shapes.Rectangle(
        width=rectangleHeight, height=rectangleWidth/2, x=screens[0].width//2 - rectangleWidth, y=screens[0].height//2 - rectangleHeight, color=wavelengthToRGB(colorToDraw, gamma), batch=batch)
elif objectToProject == "polygonTest":
    RGBColorToDraw = wavelengthToRGB(colorToDraw, gamma)
    polygonColor = [RGBColorToDraw[0],RGBColorToDraw[1],RGBColorToDraw[2],255]
    batch.add(4, pyglet.gl.GL_POLYGON, None, ('v2i',[100,600,600,600,600,100,100,100]), ('c4B',polygonColor*4))
elif objectToProject == "class":
    objectDrawn = pygletVertex(batch,4,[100, 600, 600, 600, 600, 100, 100, 100])
    batch = objectDrawn.initialDraw()
    batch = objectDrawn.changeColor(wavelengthToRGB(foregroundWavelength, gamma))
    batch = objectDrawn.movePolygon("right", 700)

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
    if symbol == key.ENTER or symbol == key.ESCAPE:
        pyglet.app.exit()
    if symbol == key._1:
        colorToDraw = visibleForegroundWavelenth
        try:
            foregroundObjectShapes[0].color = wavelengthToRGB(colorToDraw, gamma)
            foregroundObjectShapes[1].color = wavelengthToRGB(colorToDraw, gamma)
            foregroundObjectShapes[2].color = wavelengthToRGB(colorToDraw, gamma)
        except:
            pass
    if symbol == key._2:
        colorToDraw = foregroundWavelength
        try:
            foregroundObjectShapes[0].color = wavelengthToRGB(colorToDraw, gamma)
            foregroundObjectShapes[1].color = wavelengthToRGB(colorToDraw, gamma)
            foregroundObjectShapes[2].color = wavelengthToRGB(colorToDraw, gamma)
        except:
            pass
    if symbol == key.A:
        draw = 0
    if symbol == key.S:
        draw = 1
    if symbol == key.D:
        draw = 2
    if symbol == key.LEFT:
        try:
            foregroundObjectShapes[0].x -= 10
            foregroundObjectShapes[1].x -= 10
            foregroundObjectShapes[2].x -= 10
        except:
            pass
    if symbol == key.RIGHT:
        try:
            foregroundObjectShapes[0].x += 10
            foregroundObjectShapes[1].x += 10
            foregroundObjectShapes[2].x += 10
        except:
            pass

    if symbol == key.UP:
        try:
            foregroundObjectShapes[0].y += 10
            foregroundObjectShapes[1].y += 10
            foregroundObjectShapes[2].y += 10
        except:
            pass
    if symbol == key.DOWN:
        try:
            foregroundObjectShapes[0].y -= 10
            foregroundObjectShapes[1].y -= 10
            foregroundObjectShapes[2].y -= 10
        except:
            pass

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
