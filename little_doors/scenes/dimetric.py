from pprint import pprint

from pyglet import gl

from little_doors import data
from little_doors.aabb import AABB2D
from little_doors.camera import PixelCamera
from little_doors.grid import GridIndex2D
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

        # Bounding box indexes
        self.static_grid = GridIndex2D(position=(-1024, -1024), dimensions=(64, 64), cell_size=(32.0, 32.0))
        self.dynamic_grid = GridIndex2D(position=(-1024, -1024), dimensions=(64, 64), cell_size=(32.0, 32.0))

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

        # self.terrain.load_tile_data([
        #     0, 0, 0, 0, 0, 0, 0, 0,
        #     0, 0, 0, 0, 0, 0, 0, 0,
        #     0, 0, 0, 0, 0, 0, 0, 0,
        #     0, 0, 0, 0, 0, 0, 0, 0,
        #     0, 0, 0, 0, 0, 0, 0, 0,
        #     0, 0, 0, 0, 0, 0, 0, 0,
        #     0, 0, 0, 0, 0, 0, 0, 0,
        #     1, 0, 0, 0, 0, 0, 0, 0,
        # ])

        # Index bounding boxes that are not expected to change.
        for x, y in self.terrain:
            aabb2d = self.terrain.get_cell_aabb2d(x, y)
            if aabb2d is not None:
                self.static_grid.insert(aabb2d)

    def on_mouse_release(self, x, y, button, modifiers):
        print("Mouse Screen", x, y)

        x, y = self.camera.window_to_world(x, y)
        print("Mouse World", (x, y))

        query = AABB2D(x, y, 1.0, 1.0)
        print("Query", query)

        for aabb2d in self.static_grid.find(query):
            print(aabb2d)

        print("==============")
        print("")

    def on_update(self, dt):
        self.dynamic_grid.recalculate()

    def on_draw(self, context):
        self.camera.push_state()

        gl.glClear(gl.GL_COLOR_BUFFER_BIT)
        self.terrain.draw()

        self.camera.pop_state()
