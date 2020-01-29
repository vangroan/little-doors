from collections import defaultdict
from functools import reduce

import pyglet
from pyglet import gl
from pyglet.window import key

from little_doors import data, vec
from little_doors.aabb import AABB2D
from little_doors.camera import PixelCamera
from little_doors.collide import PhysicsWorld3D
from little_doors.grid import GridIndex2D, IndexGroup2D
from little_doors.player import Player
from little_doors.scene import Scene
from little_doors.tilemap import TileMap


class DimetricScene(Scene):
    """
    Test scene to visualise dimetric projection.
    """

    def __init__(self):
        # Camera
        self.camera = PixelCamera()

        # Input map
        self.inputs = defaultdict(lambda: False)

        # Tile map
        self.tilemap = TileMap((8, 8))
        self.tiles = []

        # Player
        self.player = Player(pos3d=(0.0, 0.0, 0.0))

        # Bounding box indexes
        self.static_grid = GridIndex2D(position=(-1024, -1024), dimensions=(64, 64), cell_size=(32.0, 32.0))
        self.dynamic_grid = GridIndex2D(position=(-1024, -1024), dimensions=(64, 64), cell_size=(32.0, 32.0))

        # Physics
        self.physics = PhysicsWorld3D()

        # FPS Counter
        self.fps_cursor = 0
        self.delta_times = [0.0] * 60
        self.fps_counter = pyglet.text.Label("FPS: 0", x=-100.0, y=120.0)

    def start(self, context):
        self.camera.set_position(-160.0, -64.0)

        self.tilemap.load_tile_set(data.tileset.create_tile_set())
        self.tilemap.load_tile_data([
            3, 5, 0, 1, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            1, 0, 1, 1, 3, 0, 0, 0,
            1, 0, 1, 4, 0, 0, 0, 0,
            2, 0, 2, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
        ])

        # Index bounding boxes that are not expected to change.
        for x, y in self.tilemap:
            tile = self.tilemap.get_tile(x, y)
            if tile is not None:
                if tile.aabb2d is not None:
                    self.static_grid.insert(tile.aabb2d)
                    self.physics.add(tile, tile.aabb3d.pos, tile.aabb3d.dimensions)

        self.tilemap.add_object(self.player)
        self.dynamic_grid.insert(self.player.aabb2d)

        self.physics.add(self.player, self.player.aabb3d.pos, self.player.aabb3d.dimensions)

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

    def on_key_press(self, symbol, modifiers):
        if symbol in self.inputs:
            self.inputs[symbol] = True

    def on_key_release(self, symbol, modifiers):
        if symbol in self.inputs:
            self.inputs[symbol] = False

    def on_update(self, dt):
        self.delta_times[self.fps_cursor] = dt
        self.fps_cursor += 1
        self.fps_cursor = self.fps_cursor % len(self.delta_times)
        avg_delta_time = reduce(lambda d, agg: agg + d, self.delta_times, 0.0) / len(self.delta_times)
        self.fps_counter.text = "FPS: {0:.2f}".format(1.0 / avg_delta_time if avg_delta_time > 0.0 else 0.0)

        x, y, z = 0.0, 0.0, 0.0

        # Left
        if self.inputs[key.A]:
            x -= 1.0
            y += 1.0

        # Right
        if self.inputs[key.D]:
            x += 1.0
            y -= 1.0

        # Down
        if self.inputs[key.S]:
            x -= 1.0
            y -= 1.0

        # Up
        if self.inputs[key.W]:
            x += 1.0
            y += 1.0

        # In
        if self.inputs[key.R]:
            z += 1.0

        # Out
        if self.inputs[key.F]:
            z -= 1.0

        self.player.dir = vec.normalize(x, y, z)

        # Project before actual update
        self.physics.project(self.player.aabb3d, self.player.velocity(dt))

        self.player.update(dt)

        self.dynamic_grid.recalculate()

    def on_draw(self, context):
        self.camera.push_state()

        gl.glClear(gl.GL_COLOR_BUFFER_BIT)
        self.tilemap.draw(IndexGroup2D(self.static_grid, self.dynamic_grid))

        self.fps_counter.draw()

        self.camera.pop_state()
