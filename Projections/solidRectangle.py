import pyglet
from pyglet.window import key
from pyglet import shapes

from libraries.wavelengthToRGB.wavelengthToRGB import wavelengthToRGB

# to be gdone for this project
# need to get find how to update picture of foreground object with refresh rate of monitor
# need to write a function to flip the geometry of whatever is being displayed
# need to write a funciton that generates object picturewith depth
# figure out the relative imports

# get the displays and screen information
displays = pyglet.canvas.get_display()
screens = displays.get_screens()

# instance the window object for each display
window1 = pyglet.window.Window(
    fullscreen=True, screen=screens[0], visible=False)
#window2 = pyglet.window.Window(
#    fullscreen=True, screen=screens[1], visible=False)

# same text
#label = pyglet.text.Label('Hello, world',
#                          font_name='Times New Roman',
#                          font_size=36,
#                          x=window2.width//2, y=window2.height//2,
#                          anchor_x='center', anchor_y='center')

# create a batch of shapes the program draws
batch = pyglet.graphics.Batch()

# initialize the wavelengths for colors to be used by the wavelength to RGB function
gamma = 1
#colors in wavelengths in nanometers
backgroundWavelength = 580  # yellow
foregroundWavelength = 400  # purple

# create variables that store the value of where the shapes should be drawn
background = shapes.Rectangle(
    0, 0, screens[0].width, screens[0].height, color=wavelengthToRGB(backgroundWavelength, gamma),batch=batch)

foregroundObject = shapes.Rectangle(
    0.5*(screens[0].width-screens[0].height//3), 0.5*(screens[0].height-screens[0].width//3), screens[0].height//3, screens[0].width//3, color=wavelengthToRGB(foregroundWavelength, gamma), batch=batch)
# foregroundObject.anchor_x = foregroundObject.width//2
# foregroundObject.anchor_x = foregroundObject.height//2

# create event handlers that update with drawing the batch, im not sure how often this occurs
@window1.event
def on_draw():
    window1.clear()
    batch.draw()
    

#@window2.event
#def on_draw():
#    window2.clear()
#    label.draw()

@window1.event
def on_key_press(symbol, modifiers):
    if symbol == key.ENTER or symbol == key.ESCAPE:
        pyglet.app.exit()

# set visible after all initialization
window1.set_visible()
# window2.set_visible()

# run the app
pyglet.app.run()
