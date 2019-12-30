from pprint import pprint

from pyglet import gl

from little_doors import data
from little_doors.camera import PixelCamera
from little_doors.iso import hex_bounds
from little_doors.scene import Scene
from little_doors.terrain import Terrain


class DimetricScene(Scene):
    """
    Test scene to visualise dimetric projection.
    """

    def __init__(self):
        # Camera
        self.camera = PixelCamera()

        # Tile map
        self.terrain = Terrain((8, 8))

    def start(self, context):
        self.camera.set_position(-160.0, -64.0)

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

        pprint(hex_bounds(self.terrain.get_cell_aabb3d(0, 0)))

    def on_update(self, dt):
        pass

    def on_draw(self, context):
        self.camera.push_state()

        gl.glClear(gl.GL_COLOR_BUFFER_BIT)
        self.terrain.draw()

        self.camera.pop_state()
