"""
Isometric projection.
"""
from collections import deque
from enum import Enum

from little_doors.aabb import AABB3D


def cart_to_iso(x, y, z):
    """
    Projects a 3D cartesian (x, y, z) coordinate to a 2D isometric (i, j, k) coordinate.

    >>> cart_to_iso(1, 1, 1)
    (0.0, 0.5, 1.0)

    >>> cart_to_iso(2, 3, 4)
    (0.0, 0.0, 4.0)

    >>> cart_to_iso(0, 2, 5)
    (0.0, 0.0, 5.0)
    """
    i = (float(x) - float(y)) * 0.5
    j = (float(y) + float(x)) * 0.25
    k = float(z)
    return i, j, k


def iso_to_cart():
    pass


def coord_to_hex(x, y, z):
    """
    Given a 3D cartesian coordinate, project it to hexagonal space.
    :param x:
    :param y:
    :param z:
    :return:
    """
    hex_x = float(x + z)
    hex_y = float(y + z)
    hex_h = (hex_x - hex_y) * 0.5
    hex_v = (hex_x + hex_y) * 0.25

    return hex_x, hex_y, hex_h, hex_v


def hex_bounds(aabb3d: AABB3D, pos=(0.0, 0.0, 0.0)):
    """
    Calculate the hexagonal bounds of a AABB3D, in 2D space.

    Bounds coordinates are along the x and y axes along the isometric diagonals, with
    a third axes h (horizontal) along the 2D x-axis.

    Optionally a position can be provided to offset the coordinates in 3D space.

    :param aabb3d: one AABB3D
    :param pos: Optional offset position in 3D cartesian space
    :return: Tuple with bounds (x1, x2, y1, y2, h1, h2, v1, v2)
    """
    # TODO: This function can be made more effecient by only computing the required components.
    (ox, oy, oz) = pos

    # Origin, the bottom center corner of the hexagon.
    (x_min, y_min, _, v_min) = coord_to_hex(ox + aabb3d.x,
                                            oy + aabb3d.y,
                                            oz + aabb3d.z)

    # NOTE: Top, bottom, right and left refer to the corners of the hexagon.

    # Bottom Right
    (_, _, h_max, _) = coord_to_hex(ox + aabb3d.x + aabb3d.width,
                                    oy + aabb3d.y,
                                    oz + aabb3d.z)

    # Top Right
    (x_max, _, _, _) = coord_to_hex(ox + aabb3d.x + aabb3d.width,
                                    oy + aabb3d.y,
                                    oz + aabb3d.z + aabb3d.depth)
    # Bottom Left
    (_, _, h_min, _) = coord_to_hex(ox + aabb3d.x,
                                    oy + aabb3d.y + aabb3d.height,
                                    oz + aabb3d.z)

    # Top left
    (_, y_max, _, _) = coord_to_hex(ox + aabb3d.x,
                                    oy + aabb3d.y + aabb3d.height,
                                    oz + aabb3d.z + aabb3d.depth)

    # Top
    (_, _, _, v_max) = coord_to_hex(ox + aabb3d.x + aabb3d.width,
                                    oy + aabb3d.y + aabb3d.height,
                                    oz + aabb3d.z + aabb3d.depth)

    return Hexagon(x_min, x_max, y_min, y_max, h_min, h_max, v_min, v_max)


class Hexagon(object):
    __slots__ = ('x_min', 'x_max', 'y_min', 'y_max', 'h_min', 'h_max', 'v_min', 'v_max')

    def __init__(self, x_min, x_max, y_min, y_max, h_min, h_max, v_min, v_max):
        self.x_min = x_min
        self.x_max = x_max
        self.y_min = y_min
        self.y_max = y_max
        self.h_min = h_min
        self.h_max = h_max
        self.v_min = v_min
        self.v_max = v_max

    def overlaps(self, other):
        """
        Tests whether the two given hexes (calculated using ``hex_bounds()``) overlap.

        :param other: Other hexagon
        :return: True when there is overlap
        """
        hex1_xmin, hex1_xmax, hex1_ymin, hex1_ymax, hex1_hmin, hex1_hmax, _, _ = self
        hex2_xmin, hex2_xmax, hex2_ymin, hex2_ymax, hex2_hmin, hex2_hmax, _, _ = other
        return (hex1_xmin < hex2_xmax and hex2_xmin < hex1_xmax) \
               and (hex1_ymin < hex2_ymax and hex2_ymin < hex1_ymax) \
               and (hex1_hmin < hex2_hmax and hex2_hmin < hex1_hmax)
        # return not (hex1_xmin >= hex2_xmax or hex2_xmin >= hex1_xmax) \
        #        or not (hex1_ymin >= hex2_ymax or hex2_ymin >= hex1_ymax) \
        #        or not (hex1_hmin >= hex2_hmax or hex2_hmin >= hex1_hmax)

    def __iter__(self):
        yield self.x_min
        yield self.x_max
        yield self.y_min
        yield self.y_max
        yield self.h_min
        yield self.h_max
        yield self.v_min
        yield self.v_max

    def __repr__(self):
        return "{}(x_min={}, x_max={}, y_min={}, y_max={}, h_min={}, h_max={}, v_min={}, v_max={})".format(
            self.__class__.__name__,
            self.x_min, self.x_max, self.y_min, self.y_max,
            self.h_min, self.h_max, self.v_min, self.v_max)


def is_behind(a, b) -> bool:
    """
    :type a: AABB3D
    :type b: AABB3D
    :return: True if a is behind b.
    """
    x, y, z = a.separation(b)
    if x != 0:
        return a.x < b.x
    elif y != 0:
        return a.y < b.y
    elif z != 0:
        return a.z > b.z
    return False


def is_in_front(a, b) -> bool:
    """
    :type a: AABB3D
    :type b: AABB3D
    :return: True if b is in front of a.
    """
    x, y, z = a.separation(b)
    if x != 0:
        return b.x + b.width < a.x + a.width
    elif y != 0:
        return b.y + b.height < a.y + a.height
    elif z != 0:
        return b.z + b.depth > a.y + a.depth
    return False


class NodeState(Enum):
    GREY = 0
    BLACK = 1


def topological_sort(objects, spatial_index):
    """
    :type objects: Iterator[object]
    :type spatial_index: SpatialIndex2D
    :return:
    """
    result = deque()
    enter = set(objects)
    state = {}

    lookup = {obj.aabb2d: obj for obj in enter}

    def _sort(node):
        state[node] = NodeState.GREY

        for _i, _j, k in spatial_index.find(node.aabb2d):
            nk = lookup.get(k, None)
            sk = state.get(nk, None)

            if not is_behind(nk.aabb3d, node.aabb3d):
                continue

            if sk == NodeState.GREY:
                # raise ValueError("cycle")
                continue
            if sk == NodeState.BLACK:
                continue

            enter.discard(nk)
            _sort(nk)

        result.appendleft(node)
        state[node] = NodeState.BLACK

    while enter:
        _sort(enter.pop())

    return result
