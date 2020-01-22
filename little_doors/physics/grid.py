from collections import defaultdict
from math import floor, ceil
from pprint import pprint
from typing import Tuple, Iterator, Any

from little_doors.physics.aabb import AABB3D


# TODO: Consider cell size in calculations


class GridIndex3D(object):
    """
    Spatial index that forms a voxel volume, storing 3-dimensional axis aligned
    bounding boxes in a fixed grid. Bounding boxes are stored in buckets arranged
    into grid cells, with boxes that overlap multiple cells stored in each
    overlapped cell.
    """

    def __init__(self, cell_size=(1.0, 1.0, 1.0)):
        self._cell_size = cell_size
        self._buckets = defaultdict(lambda: set())

    @staticmethod
    def bounds_to_cell(x, y, z, width, height, depth) -> Tuple[int, int, int, int, int, int]:
        """
        Given a bounding box, return the minimum and maximum cell indexes the box overlaps.

        :return: The minimum and maximum cell indexes. (x_min, y_min, z_min, x_max, y_max, z_max)
        """

        # Lower bounds (i1, j1, k1)
        return (int(floor(x)), int(floor(y)), int(floor(z)),
                # Upper bounds (i2, j2, k2)
                int(ceil(x + width)),
                int(ceil(y + height)),
                int(ceil(z + depth)))

    @staticmethod
    def cells_overlapped(aabb3d) -> Iterator[Tuple[int, int]]:
        """
        Helper to determine which cells the given bounding box overlaps.

        :param aabb3d: Target bounding box to test against.
        :return: Iterator yielding tuples containing cell indexes.
        """
        i1, j1, k1, i2, j2, k2 = GridIndex3D.bounds_to_cell(*aabb3d)
        for k in range(k1, k2):
            for j in range(j1, j2):
                for i in range(i1, i2):
                    yield i, j, k

    def insert(self, item, aabb3d) -> int:
        """
        Inserts an item into the grid's index, using the given bounding box
        to choose which cells the item belongs to.

        :return:
        """
        count = 0

        for i, j, k in self.cells_overlapped(aabb3d):
            self._buckets[(i, j, k)].add((item, aabb3d))
            count += 1

        return count

    def purge(self, item):
        raise NotImplementedError()

    def update(self, item):
        """
        Change the position and dimensions of a bounding box, updating
        potentially changing the cell buckets it's in.
        """
        raise NotImplementedError()

    def find(self, x, y, z, width, height, depth) -> Iterator[Tuple[Any, AABB3D]]:
        """
        Query the grid for items and bounding boxes that are
        close neighbours to the given bounds.

        :return: Iterator that yields tuples containing
            items their associated bounding boxes.
        """
        i1, j1, k1, i2, j2, k2 = self.bounds_to_cell(x, y, z, width, height, depth)

        for k in range(k1, k2):
            for j in range(j1, j2):
                for i in range(i1, i2):

                    if (i, j, k) in self._buckets:
                        cell = self._buckets[i, j, k]
                        for item_and_aabb3d in cell:
                            yield item_and_aabb3d


# -----------
# -- Tests --
# -----------

def test_insert():
    # assume
    grid = GridIndex3D()
    item = object()
    aabb3d = AABB3D(0.5, 0.5, 0.5, 1.0, 1.0, 1.0)

    # act
    count = grid.insert(item, aabb3d)

    # assert
    assert count == 8, "Unexpected count of cells returned"
