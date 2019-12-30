class AABB3D(object):
    """
    3-Dimensional axis aligned bounding box.
    """
    __slots__ = ('x', 'y', 'z', 'width', 'height', 'depth')

    def __init__(self, x, y, z, width, height, depth):
        """
        :type x: float
        :type y: float
        :type z: float
        :type width: float
        :type height: float
        :type depth: float
        """
        self.x = x
        self.y = y
        self.z = z
        self.width = width
        self.height = height
        self.depth = depth

    def __repr__(self):
        return "{}(x={}, y={}, z={}, width={}, height={}, depth={})".format(
            self.__class__.__name__, self.x, self.y, self.z, self.width, self.height, self.depth)


class AABB2D(object):
    """
    2-Dimensional axis aligned bounding box.
    """
    __slots__ = ('x', 'y', 'width', 'height')

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
