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

    def separation(self, other):
        """
        Determines how this bounding box and another are separated, described as a tuple that can contain -1, 0 or 1.

        :param other: Another AABB3D box.
        :return: Tuple with three elements indicating on which side the other box is to this box.
        """
        x = 0
        if self.x >= other.x + other.width:
            x = -1
        elif other.x >= self.x + self.width:
            x = 1

        y = 0
        if self.y >= other.y + other.height:
            y = -1
        elif other.y >= self.y + self.height:
            y = 1

        z = 0
        if self.z >= other.z + other.depth:
            z = -1
        elif other.z >= self.z + self.depth:
            z = 1

        return x, y, z

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

    def overlap(self, other):
        """
        Tests whether this bounding box overlaps with the other given box-like.

        :param other: Iterable that unpacks into (x, y, width, height)
        :return: True if they overlap
        """
        (x1, y1, w1, h1) = self
        (x2, y2, w2, h2) = other
        raise NotImplementedError()

    def __iter__(self):
        yield self.x
        yield self.y
        yield self.width
        yield self.height
