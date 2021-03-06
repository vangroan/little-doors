from pyglet import gl
from pyglet.window import key

from little_doors import data
from little_doors.camera import PixelCamera, pyglet
from little_doors.grid import GridIndex2D
from little_doors.iso import cart_to_iso
from little_doors.player import Player
from little_doors.scene import Scene
from little_doors.tilemap import TileMap
from little_doors import vec


class PlayScene(Scene):
    def __init__(self):
        self.tilemap = TileMap((8, 8))
        self.camera = PixelCamera()
        self.player = Player(pos3d=(0.0, 0.0, 1.0))

        # Input map
        self.inputs = {
            key.A: False,
            key.D: False,
            key.W: False,
            key.S: False,
        }

        # Bounding box indexes
        self.static_grid = GridIndex2D(position=(-1024, -1024), dimensions=(64, 64), cell_size=(32.0, 32.0))

        # Text labels for cartesian coordinates
        (tile_width, tile_height) = self.tilemap.tile_size_2d
        self.origin_text = pyglet.text.Label('0, 0, 0', x=0, y=0, align='center', anchor_x='center', anchor_y='top')

        (i1, j1, _k1) = cart_to_iso(8.0, 0.0, 0.0)
        self.origin_text_x = pyglet.text.Label('8, 0, 0', x=i1 * tile_width, y=j1 * tile_height, align='center',
                                               anchor_x='center', anchor_y='top')

        (i2, j2, _k2) = cart_to_iso(0.0, 8.0, 0.0)
        self.origin_text_y = pyglet.text.Label('0, 8, 0', x=i2 * tile_width, y=j2 * tile_height, align='center',
                                               anchor_x='center', anchor_y='top')

    def start(self, context):
        print("Start Play Scene")
        self.camera.set_position(-160.0, -64.0)

        self.tilemap.load_tile_set(data.tileset.create_tile_set())
        self.tilemap.load_tile_data([
            1, 1, 1, 1, 1, 1, 1, 1,
            1, 0, 0, 1, 1, 0, 0, 1,
            1, 0, 1, 1, 1, 1, 0, 1,
            1, 1, 1, 0, 0, 1, 1, 1,
            1, 1, 1, 0, 0, 1, 1, 1,
            1, 0, 1, 1, 1, 1, 0, 1,
            1, 0, 0, 1, 1, 0, 0, 1,
            1, 1, 1, 1, 1, 1, 1, 1,
        ])

        # Index bounding boxes that are not expected to change.
        for x, y in self.tilemap:
            aabb2d = self.tilemap.get_cell_aabb2d(x, y)
            if aabb2d is not None:
                self.static_grid.insert(aabb2d)

    def on_key_press(self, symbol, modifiers):
        if symbol in self.inputs:
            self.inputs[symbol] = True

    def on_key_release(self, symbol, modifiers):
        if symbol in self.inputs:
            self.inputs[symbol] = False

    def on_update(self, dt):
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

        self.player.dir = vec.normalize(x, y, z)
        self.player.update(dt)

    def on_draw(self, context):
        self.camera.push_state()

        gl.glClear(gl.GL_COLOR_BUFFER_BIT)
        self.tilemap.draw()
        self.player.draw()
        self.origin_text.draw()
        self.origin_text_x.draw()
        self.origin_text_y.draw()

        self.camera.pop_state()
