from typing import Tuple


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

    def separation(self, other) -> Tuple[float, float, float]:
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

    def intersects(self, other) -> bool:
        """
        Checks whether this bounding box intersects with another bounding box or box-like object.

        :param other: Another AABB3D box or tuple of bounding box components.
        :return: True when bounding boxes intersect.
        """
        ox_min, oy_min, oz_min, ow, oh, od = other
        ox_max = ox_min + ow
        oy_max = oy_min + oh
        oz_max = oz_min + od
        return (ox_min < self.x + self.width and self.x < ox_max) \
               and (oy_min < self.y + self.height and self.y < oy_max) \
               and (oz_min < self.z + self.depth and self.z < oz_max)

    @property
    def dimensions(self) -> Tuple[float, float, float]:
        """
        The 3D size of the bounding box as a tuple of components.
        """
        return self.width, self.height, self.depth

    @property
    def position(self) -> Tuple[float, float, float]:
        """
        The 3D position of the bounding box as a tuple of components.
        """
        return self.x, self.y, self.z

    @position.setter
    def position(self, pos):
        self.x, self.y, self.z = pos

    def __iter__(self):
        yield self.x
        yield self.y
        yield self.z
        yield self.width
        yield self.height
        yield self.depth

    def __repr__(self):
        return "{}(x={}, y={}, z={}, width={}, height={}, depth={})".format(
            self.__class__.__name__, self.x, self.y, self.z, self.width, self.height, self.depth)
