
class AABB3D(object):
    """
    3-Dimensional axis aligned bounding box.
    """
    __slots__ = ('_x', '_y', '_z', '_width', '_height', '_depth')

    def __init__(self, x, y, z, width, height, depth):
        self._x = x
        self._y = y
        self._z = z
        self._width = width
        self._height = height
        self._depth = depth


class AABB2D(object):
    """
    2-Dimensional axis aligned bounding box.
    """
    __slots__ = ('_x', '_y', '_width', '_height')

    def __init__(self, x, y, width, height):
        self._x = x
        self._y = y
        self._width = width
        self._height = height
