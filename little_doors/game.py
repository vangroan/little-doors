from pyglet.gl import *

from little_doors.camera import PixelCamera
from little_doors.terrain import Terrain
from little_doors import data


class Game:
    def __init__(self):
        self._terrain = Terrain((8, 8))
        self._window = None
        self.camera = PixelCamera()

    def init(self):
        self._terrain.load_tile_set(data.tileset.create_tile_set())
        self._terrain.load_tile_data([
            1, 1, 1, 1, 1, 1, 1, 1,
            1, 0, 0, 1, 1, 0, 0, 1,
            1, 0, 1, 1, 1, 1, 0, 1,
            1, 1, 1, 0, 0, 1, 1, 1,
            1, 1, 1, 0, 0, 1, 1, 1,
            1, 0, 1, 1, 1, 1, 0, 1,
            1, 0, 0, 1, 1, 0, 0, 1,
            1, 1, 1, 1, 1, 1, 1, 1,
        ])

    def draw(self):
        self.camera.push_state()

        glClear(GL_COLOR_BUFFER_BIT)
        self._terrain.draw()

        self.camera.pop_state()
