import pyglet

from little_doors.context import Context
from little_doors.game import Game

game = Game()
window = pyglet.window.Window(
    caption="Little Doors",
    width=640,
    height=480,
)


@window.event
def on_mouse_motion(x, y, dx, dy):
    game.on_mouse_motion(x, y, dx, dy)


@window.event
def on_mouse_press(x, y, button, modifiers):
    game.on_mouse_press(x, y, button, modifiers)


@window.event
def on_mouse_release(x, y, button, modifiers):
    game.on_mouse_release(x, y, button, modifiers)


@window.event
def on_draw():
    window.clear()
    game.on_draw()


if __name__ == "__main__":
    with Context(game, window) as _ctx:
        game.start()
        pyglet.clock.schedule_interval(game.on_update, 1.0 / 60.0)
        pyglet.app.run()

        # Explicitly unschedule update to avoid weak ref exception
        pyglet.clock.unschedule(game.on_update)
