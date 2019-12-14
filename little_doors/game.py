from little_doors.scene import SceneStack
from little_doors.scenes.play import PlayScene


class Game:
    def __init__(self):
        self._window = None
        self._scenes = SceneStack()

    def start(self):
        self._scenes.push(PlayScene())

    def draw(self):
        scene = self._scenes.top
        if scene:
            scene.draw(None)
