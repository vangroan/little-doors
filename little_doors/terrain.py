import pyglet

from little_doors.iso import cart_to_iso


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
        self._size = size
        self._data = [0] * (size[0] * size[1])
        self._tile_set = dict()
        self._sprites = [None] * (size[0] * size[1])
        self._batch = pyglet.graphics.Batch()

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
        data_index = x + y * self._size[0]
        self._data[data_index] = tile_index

        if self._sprites[data_index]:
            self._sprites[data_index].delete()
            self._sprites[data_index] = None

        # Only create sprite when not zero
        if tile_index:
            tile = self._tile_set.get(tile_index, None)
            if not tile:
                raise TileSetError("tile set does not contain tile for index %s" % tile_index)

            (i, j, _k) = cart_to_iso(x, y, 0)
            self._sprites[data_index] = pyglet.sprite.Sprite(tile.image, x=i * 32, y=j * 32)

    def draw(self):
        for sprite in self._sprites:
            if sprite:
                sprite.draw()
