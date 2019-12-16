from pyglet import gl

from little_doors import data
from little_doors.camera import PixelCamera
from little_doors.player import Player
from little_doors.scene import Scene
from little_doors.terrain import Terrain


class PlayScene(Scene):
    def __init__(self):
        self.terrain = Terrain((8, 8))
        self.camera = PixelCamera()
        self.player = Player(pos3d=(0.0, 0.0, 1.0))

    def start(self, context):
        print("Start Play Scene")
        self.camera.set_position(-(32.0 * 4.5), -(32.0 * 1.5))

        self.terrain.load_tile_set(data.tileset.create_tile_set())
        self.terrain.load_tile_data([
            1, 1, 1, 1, 1, 1, 1, 1,
            1, 0, 0, 1, 1, 0, 0, 1,
            1, 0, 1, 1, 1, 1, 0, 1,
            1, 1, 1, 0, 0, 1, 1, 1,
            1, 1, 1, 0, 0, 1, 1, 1,
            1, 0, 1, 1, 1, 1, 0, 1,
            1, 0, 0, 1, 1, 0, 0, 1,
            1, 1, 1, 1, 1, 1, 1, 1,
        ])

    def on_update(self, dt):
        self.player.update(dt)

    def on_draw(self, context):
        self.camera.push_state()

        gl.glClear(gl.GL_COLOR_BUFFER_BIT)
        self.terrain.draw()
        self.player.draw()

        self.camera.pop_state()
