
class AABB3D(object):
    """
    3-Dimensional axis aligned bounding box.
    """
    __slots__ = ('_x', '_y', '_width', '_height')

    def __init__(self, x, y, width, height):
        self._x = x
        self._y = y
        self._width = width
        self._height = height
