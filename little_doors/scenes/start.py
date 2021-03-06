import pyglet

from little_doors.camera import PixelCamera
from little_doors.context import Context
from little_doors.menu import Menu, MenuButton
from little_doors.scene import Scene
from little_doors.scenes.dimetric import DimetricScene
from little_doors.scenes.play import PlayScene


class StartScene(Scene):
    def __init__(self):
        self.camera = PixelCamera()

        self.menu = Menu()
        self.menu.add(MenuButton(label="Play", x=96, y=176, on_release=self.on_play_release))
        self.menu.add(MenuButton(label="Dimetric Test", x=96, y=136, on_release=self.on_dimetric_test_release))
        self.menu.add(MenuButton(label="Quit", x=96, y=96, on_release=self.on_quit_release))

    @staticmethod
    def on_play_release(*args, **kwargs):
        ctx = Context.current()
        ctx.game.scenes.push(PlayScene())

    @staticmethod
    def on_dimetric_test_release(*args, **kwargs):
        ctx = Context.current()
        ctx.game.scenes.push(DimetricScene())

    @staticmethod
    def on_quit_release(*args, **kwargs):
        pyglet.app.exit()

    def on_mouse_press(self, x, y, button, modifiers):
        x, y = self.camera.window_to_world(x, y)
        self.menu.on_mouse_press(x, y, button, modifiers)

    def on_mouse_release(self, x, y, button, modifiers):
        x, y = self.camera.window_to_world(x, y)
        self.menu.on_mouse_release(x, y, button, modifiers)

    def on_mouse_motion(self, x, y, dx, dy):
        x, y = self.camera.window_to_world(x, y)
        self.menu.on_mouse_motion(x, y, dx, dy)

    def on_draw(self, ctx):
        self.camera.push_state()
        self.camera.clear()
        self.menu.on_draw()
        self.camera.pop_state()
