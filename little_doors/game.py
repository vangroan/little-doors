from little_doors.scene import SceneStack
from little_doors.scenes.start import StartScene


class Game:
    def __init__(self):
        self._window = None
        self._scenes = SceneStack()

    @property
    def scenes(self):
        return self._scenes

    def start(self):
        self._scenes.push(StartScene())

    def on_mouse_press(self, x, y, button, modifiers):
        scene = self._scenes.top
        if scene:
            scene.on_mouse_press(x, y, button, modifiers)

    def on_mouse_release(self, x, y, button, modifiers):
        scene = self._scenes.top
        if scene:
            scene.on_mouse_release(x, y, button, modifiers)

    def on_mouse_motion(self, x, y, dx, dy):
        scene = self._scenes.top
        if scene:
            scene.on_mouse_motion(None, x, y, dx, dy)

    def on_draw(self):
        scene = self._scenes.top
        if scene:
            scene.on_draw(None)
