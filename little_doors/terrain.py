from copy import deepcopy
from enum import Enum
from typing import Optional, List, Tuple

import pyglet

from little_doors.aabb import AABB3D, AABB2D
from little_doors.iso import cart_to_iso
from little_doors.mixins import MapObjectMixin
from little_doors.tile import Tile


class DrawableKind(Enum):
    TILE = 1
    OBJECT = 2


class TileSetError(Exception):
    """
    Error while interacting with the tile map's tile set.
    """


class TerrainError(Exception):
    """
    Error while working with terrain data.s
    """


class Terrain(object):
    """
    2-Dimensional tile map.
    """

    def __init__(self, size):
        """
        :param size: Tuple that contains the width and height of the map.
        """
        length = size[0] * size[1]

        self._size = size
        self._tile_size_2d = (32.0, 32.0)
        # self._data = [0] * length
        self._tiles = [None] * length  # type: List[Optional[Tile]]
        self._tile_set = dict()
        self._objects = []  # type: List[object]
        self._sprites = [None] * length  # type: List[Optional[pyglet.sprite.Sprite]]
        self._aabb3d = [None] * length  # type: List[Optional[AABB3D]]
        self._aabb2d = [None] * length  # type: List[Optional[AABB2D]]
        self._draw_order = []  # type: List[Tuple[int, int, int]]

    @property
    def tile_size_2d(self):
        """
        The standard size of a tile sprite in 2D screen space.
        """
        return 32.0, 32.0

    def load_tile_set(self, tile_set):
        self._tile_set.update(tile_set)

    def load_tile_data(self, data):
        if len(data) != self._size[0] * self._size[1]:
            raise TerrainError("data length does not fit in terrain")

        for y in range(self._size[1]):
            for x in range(self._size[0]):
                tile_index = data[x + y * self._size[0]]
                self.set_cell(x, y, tile_index)

    def set_cell(self, x, y, tile_index):
        """
        Sets the cell at the given position to the tile given via the tile index.

        :type x: int
        :type y: int
        :type tile_index: int
        """
        data_index = x + y * self._size[0]  # type: int
        # self._data[data_index] = tile_index
        #
        # if self._sprites[data_index]:
        #     self._sprites[data_index].delete()
        #     self._sprites[data_index] = None

        # Release resources
        if self._tiles[data_index]:
            self._tiles[data_index].delete()
            self._tiles[data_index] = None

        # Only create sprite when not zero
        if tile_index:
            tile_prototype = self._tile_set.get(tile_index, None)  # type: Optional[Tile]
            if not tile_prototype:
                raise TileSetError("tile set does not contain tile for index %s" % tile_index)

            tile_w, tile_h = self._tile_size_2d
            i, j, _k = cart_to_iso(x, y, 0)
            ax, ay = tile_prototype.anchor
            tile_x, tile_y = i * tile_w - ax, j * tile_h - ay

            tile = deepcopy(tile_prototype)
            tile.sprite = pyglet.sprite.Sprite(tile.image, tile_x, tile_y)
            tile.aabb3d.pos = float(x), float(y), 0.0
            tile.aabb2d.pos = tile_x, tile_y
            self._tiles[data_index] = tile
            # self._sprites[data_index] = pyglet.sprite.Sprite(tile.image, tile_x, tile_y)

            # Currently only supports a single level, so everything is on z-level 0
            # self._aabb3d[data_index] = AABB3D(float(x), float(y), 0.0, tile.size[0], tile.size[1], tile.size[2])
            # self._aabb2d[data_index] = AABB2D(tile_x, tile_y, tile_w, tile_h)

    def get_tile(self, x, y):
        return self._tiles[x + y * self._size[0]]

    def get_sprite(self, x, y):
        return self._sprites[x + y * self._size[0]]

    def get_cell_aabb3d(self, x, y):
        return self._aabb3d[x + y * self._size[0]]

    def get_cell_aabb2d(self, x, y):
        return self._aabb2d[x + y * self._size[0]]

    def add_object(self, obj):
        """
        Adds an object, to be managed and drawn by the tile map.

        :type obj: MapObjectMixin
        :param obj:
        """
        self._objects.append(obj)

    def _build_draw_order(self):
        tiles = filter(lambda e: self.get_sprite(e[1], e[2]),
                       ((DrawableKind.TILE, coord[0], coord[1]) for idx, coord in enumerate(self)))

        # TODO: Determine
        objects = ((DrawableKind.OBJECT, 0, 0) for obj in self._objects)
        # tiles.sort(key=create_dimetric_cmp(self.terrain), reverse=True)

    def sort(self, key_func):
        """
        Sorts the drawables in an order that they can be rendered using the painter's algorithm (back to front).

        :type key_func: Callable[[Tuple[DrawableKind, int, int]], int]
        :param key_func: A callable that takes a tuple and returns an integer.
        """
        pass

    def draw(self):
        (width, height) = self._size
        for x in range(width - 1, -1, -1):
            for y in range(height - 1, -1, -1):
                tile = self._tiles[x + y * width]  # type: Optional[Tile]
                if tile:
                    tile.sprite.draw()

    def __iter__(self):
        for y in range(self._size[1]):
            for x in range(self._size[0]):
                yield x, y
