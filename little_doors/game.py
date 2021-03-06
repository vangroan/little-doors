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
            scene.on_mouse_motion(x, y, dx, dy)

    def on_key_press(self, symbol, modifiers):
        scene = self._scenes.top
        if scene:
            scene.on_key_press(symbol, modifiers)

    def on_key_release(self, symbol, modifiers):
        scene = self._scenes.top
        if scene:
            scene.on_key_release(symbol, modifiers)

    def on_update(self, dt):
        scene = self._scenes.top
        if scene:
            scene.on_update(dt)

    def on_draw(self):
        scene = self._scenes.top
        if scene:
            scene.on_draw(None)
