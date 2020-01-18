from little_doors.aabb import AABB3D, AABB2D
from little_doors.mixins import MapObjectMixin

# Size of tile along each axis when no size is specified.
DEFAULT_DIMENSION = 1.0
DEFAULT_TILE_SIZE = 32.0


class Tile(object):
    __slots__ = ('index', 'name', 'resource_filename', 'sprite', 'image', '_aabb3d', 'aabb2d', 'anchor', 'depth')

    def __init__(self, index, name='Tile', resource_filename='', dimension=None, tile_size=None,
                 anchor=(0.0, 0.0), depth=0.0):
        self.index = index
        self.name = name
        self.resource_filename = resource_filename
        self.sprite = None
        self.image = None
        self._aabb3d = AABB3D(0.0, 0.0, 0.0, DEFAULT_DIMENSION, DEFAULT_DIMENSION, DEFAULT_DIMENSION) \
            if dimension is None else AABB3D(0.0, 0.0, 0.0, *dimension)
        self.aabb2d = AABB2D(0.0, 0.0, DEFAULT_TILE_SIZE, DEFAULT_TILE_SIZE) \
            if tile_size is None else AABB2D(0.0, 0.0, *tile_size)
        self.anchor = anchor
        self.depth = depth

    @property
    def aabb3d(self):
        return self._aabb3d

    @property
    def size(self):
        return self.aabb3d.dimensions

    def delete(self):
        if self.sprite:
            self.sprite.delete()

    def draw(self):
        if self.sprite:
            self.sprite.draw()
