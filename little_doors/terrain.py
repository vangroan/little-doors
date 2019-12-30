from typing import Optional, Any, List, Union

import pyglet

from little_doors.aabb import AABB3D
from little_doors.iso import cart_to_iso
from little_doors.tile import Tile


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
        self._data = [0] * length
        self._tile_set = dict()
        self._sprites = [None] * length  # type: List[Optional[pyglet.sprite.Sprite]]
        self._aabbs = [None] * length  # type: List[Optional[AABB3D]]
        self._batch = pyglet.graphics.Batch()

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
        """
        data_index = x + y * self._size[0]  # type: int
        self._data[data_index] = tile_index

        if self._sprites[data_index]:
            self._sprites[data_index].delete()
            self._sprites[data_index] = None

        # Only create sprite when not zero
        if tile_index:
            tile = self._tile_set.get(tile_index, None)  # type: Optional[Tile]
            if not tile:
                raise TileSetError("tile set does not contain tile for index %s" % tile_index)

            (i, j, _k) = cart_to_iso(x, y, 0)
            (ax, ay) = tile.anchor
            self._sprites[data_index] = pyglet.sprite.Sprite(tile.image, x=i * 32 - ax, y=j * 32 - ay)

            size = tile.size  # type: Optional[tuple[float, float]]
            self._aabbs[data_index] = AABB3D(x, y, 0, tile.size[0], tile.size[1], 0)

    def draw(self):
        (width, height) = self._size
        for x in range(width - 1, -1, -1):
            for y in range(height - 1, -1, -1):
                sprite = self._sprites[x + y * width]  # type: Optional[pyglet.sprite.Sprite]
                if sprite:
                    sprite.draw()
