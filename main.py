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
    game.start()
    
    pyglet.app.run()
