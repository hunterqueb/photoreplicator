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
# need to write a function to flip the geometry of whatever is being displayed
# figure out the relative imports

# prints 30 pixels/mm
# accuracy of 33 microns

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

NUM_OF_POLYGONS = 5

foregroundObjectShapes = [None]*NUM_OF_POLYGONS

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
    # in order to draw a polygon, you need to follow this format
    # first define the objectDrawn object using the class, pass in the batch, vertex count, and vertices locations
    # the idea is we can find test however we want.
    polygon = [100, 700, 300, 700, 300, 100, 100, 100]
    polygonVertexNum = int(len(polygon)/2)

    objectDrawn = pygletVertex(batch, polygonVertexNum, polygon)
    # now draw the initial batches
    vertexList = objectDrawn.initialDraw(batch)
    
    # when you want to move the object to the right, you have to follow this general format
    # you must first delete the vertexList
    vertexList.delete()
    # then you call the method to redraw the polygon
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
    if symbol == key.A:
        draw = 0
    if symbol == key.S:
        draw = 1
    if symbol == key.D:
        draw = 2
    if symbol == key.LEFT:
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
