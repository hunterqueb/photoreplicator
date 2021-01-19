import pyglet
from pyglet import shapes


displays = pyglet.canvas.get_display()
screens = displays.get_screens()

window1 = pyglet.window.Window(
    fullscreen=True, screen=screens[0], visible=False)
window2 = pyglet.window.Window(
    fullscreen=True, screen=screens[1], visible=False)


label = pyglet.text.Label('Hello, world',
                          font_name='Times New Roman',
                          font_size=36,
                          x=window2.width//2, y=window2.height//2,
                          anchor_x='center', anchor_y='center')

batch = pyglet.graphics.Batch()

red_sequare = shapes.Rectangle(
    150, 240, 200, 20, color=(255, 55, 55), batch=batch)
green_sequare = shapes.Rectangle(
    175, 220, 150, 20, color=(55, 255, 55), batch=batch)
blue_sequare = shapes.Rectangle(
    200, 200, 100, 20, color=(55, 55, 255), batch=batch)

@window1.event
def on_draw():
    window1.clear()
    batch.draw()

@window2.event
def on_draw():
    window2.clear()
    label.draw()


@window1.event
def on_key_press(symbol, modifiers):
    pyglet.app.exit()


window1.set_visible()
window2.set_visible()

pyglet.app.run()
