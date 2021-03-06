# noinspection PyUnresolvedReferences
from typing import Union, Tuple

from typing_extensions import Protocol


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

    @property
    def dimensions(self):
        return self.width, self.height, self.depth

    @property
    def pos(self):
        return self.x, self.y, self.z

    @pos.setter
    def pos(self, pos):
        self.x, self.y, self.z = pos

    def __repr__(self):
        return "{}(x={}, y={}, z={}, width={}, height={}, depth={})".format(
            self.__class__.__name__, self.x, self.y, self.z, self.width, self.height, self.depth)


class AABB2D(object):
    """
    2-Dimensional axis aligned bounding box.
    """
    __slots__ = ('x', 'y', 'width', 'height')

    def __init__(self, x, y, width, height):
        """
        :type x: float
        :type y: float
        :type width: float
        :type height: float
        """
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    @property
    def pos(self) -> Tuple[float, float]:
        """
        Bounding box position.
        """
        return self.x, self.y

    @pos.setter
    def pos(self, pair):
        """
        :type pair: Tuple[float, float]
        """
        self.x, self.y = pair

    def overlap(self, other):
        """
        Tests whether this bounding box overlaps with the other given box-like.

        :type other: Union[AABB2D, Tuple[float, float, float, float]]
        :param other: Generator that unpacks into (x, y, width, height)
        :return: True if they overlap
        """
        (x1, y1, w1, h1) = self
        (x2, y2, w2, h2) = other
        return x1 <= x2 + w2 and x2 <= x1 + w1 and y1 <= y2 + h2 and y2 <= y1 + h1

    def __iter__(self):
        yield self.x
        yield self.y
        yield self.width
        yield self.height

    def __repr__(self):
        return "{}(x={}, y={}, width={}, height={})".format(
            self.__class__.__name__, self.x, self.y, self.width, self.height)


class Spatial3D(Protocol):
    """
    Bounding box that reflects the object's position and size in 3-dimensional space.

    Should return a reference to the bounding box object, and not a copy, because the reference is
    used as the box's identity in collections and spatial indexes.

    The position of the box should be kept up to date with the object's position in 3D space.

    :return: Reference to a 3D bounding box.
    """
    aabb3d: AABB3D


class Spatial2D(Protocol):
    """
    Bounding box that reflects the object's position and size in 2-dimensional space.

    The 2D space is in world space, not screen space, before it has been transformed by the camera.

    Should return a reference to the bounding box object, and not a copy, because the reference is
    used as the box's identity in collections and spatial indexes.

    The position of the box should be kept up to date with the object's position in 2D space.

    :return: Reference to a 2D bounding box.
    """
    aabb2d: AABB2D
