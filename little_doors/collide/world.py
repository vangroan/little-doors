from typing import Tuple

from little_doors.collide import vector3
from little_doors.collide.grid import GridIndex3D
from .aabb import AABB3D


class PhysicsWorld3D(object):
    def __init__(self):
        self._bounding_boxes = {}
        self._spatial_index = GridIndex3D()

    def get_bounding_box(self, item) -> Tuple[float, float, float, float, float, float]:
        """
        Retrieves the bounding box components of the given item.

        Does not return a reference to the AABB3D because it's for
        internal use, and the world needs to keep it private to
        maintain its integrity.

        :param item: Any arbitrary value that has been added to the world.
        :return: Tuple of bounding box components. Its position and dimensions.
        :raise KeyError: When the item does not exist in the world.
        """
        aabb3d = self._bounding_boxes[item]
        x, y, z = aabb3d.position
        w, h, d = aabb3d.dimensions
        return x, y, z, w, h, d

    def add(self, item, position, size):
        """
        Adds an item to the world. The item must be hashable.

        :type item: Any
        :type position: Tuple[float, float, float]
        :type size: Tuple[float, float, float]
        :type item: Any arbitrary value that can be identified using simple equality.
        :param position: 3D world position of bounding box.
        :param size: 3D dimensions of bounding box.
        :raise ValueError: When item already exists in the world.
        :raise TypeError: When item is not hashable.
        """
        if item in self._bounding_boxes:
            raise ValueError("Item %s already exists in the world" % item)

        x, y, z = position
        w, h, d = size
        aabb3d = AABB3D(x, y, z, w, h, d)
        self._bounding_boxes[item] = aabb3d

        self._spatial_index.insert(item, aabb3d)

    def remove(self, item):
        self._bounding_boxes.pop(item)
        # TODO: Remove from grid index

    def project(self, aabb3d, delta_position):
        """
        :type aabb3d: AABB3D
        :type delta_position: Tuple[float, float, float]
        :param aabb3d:
        :param delta_position: A vector that encodes the direction and
            length that the bounding box will move.
        :return:
        """
        # Projected bounding box location; minimum and maximum bounds
        w, h, d = aabb3d.dimensions
        dx_min, dy_min, dz_min = vector3.add(aabb3d.position, delta_position)
        dx_max, dy_max, dz_max = dx_min + w, dy_min + h, dz_min + d

        for neigh_item, neigh_aabb3d in self._spatial_index.find(dx_min, dy_min, dz_min, w, h, d):
            # Ignore self
            if neigh_aabb3d is aabb3d:
                continue

            # Test neighbour against the projected bounding
            # box for collision.
            if neigh_aabb3d.intersects((dx_min, dy_min, dz_min, w, h, d)):
                print("Intersects with ({}, {})".format(neigh_item, neigh_aabb3d))

            # TODO: Backtrack until not colliding
            # TODO: Determine separating axis
            # TODO: Get separation normal
            # TODO: Call resolution handler

    def step(self, delta_time):
        # TODO: Decide whether the world will integrate forces, or if it will purely be a collision library.
        raise NotImplementedError()

    def __contains__(self, item):
        return item in self._bounding_boxes


def test_world_add():
    """
    Should add any arbitrary item to the world.
    """
    # assume
    world = PhysicsWorld3D()
    item_a = ('A',)
    item_b = ('B',)

    # act
    world.add(item_a, (0.0, 0.0, 0.0), (1.0, 1.0, 1.0))
    world.add(item_b, (3.0, 3.0, 3.0), (2.0, 2.0, 2.0))

    # assert
    assert (0.0, 0.0, 0.0, 1.0, 1.0, 1.0) == world.get_bounding_box(item_a)
    assert (3.0, 3.0, 3.0, 2.0, 2.0, 2.0) == world.get_bounding_box(item_b)
