import pyglet
from little_doors.game import Game

game = Game()
window = pyglet.window.Window(
    caption="Little Doors",
    width=640,
    height=480,
)


@window.event
def on_draw():
    window.clear()
    game.draw()


if __name__ == "__main__":
    game.init()
    game.camera.set_position(-640 * 0.25, -480 * 0.10)

    pyglet.app.run()
