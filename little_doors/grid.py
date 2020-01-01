from math import floor
from typing import Tuple, List, Optional, Set

from little_doors.aabb import AABB2D


class GridIndex2D(object):
    """
    Spatial index that stores 2D axis aligned bounding boxes in a fixed grid. Bounding boxes are stored in cells, and
    boxes that overlap multiple cells are stored in each overlapped cell.

    The index keeps object references to the inserted bounding boxes. If the properties of the boxes change the index
    is no longer correct. The method ``recalculate()`` must be called to moved bounding boxes to the correct cells.

    Neighbouring bounding boxes can be queried by coordinate or bounding box.

    Use case is for indexing objects that change position frequently, at least every frame.
    """

    def __init__(self, position=(0.0, 0.0), dimensions=(16, 16), cell_size=(32.0, 32.0)):
        """
        Creates a new empty index.

        :param position: 2-Dimensional position of the grid, in pixel space. Used
            as the offset to cover a world or screen area that extends into the negative
            coordinates. Example: ``(-1024.0, -1024.0)``
        :param dimensions: Number of columns and rows in the grid.
        :param cell_size: 2-Dimensional width and height of each cell in the grid.
        """
        # The spatial area that the index covers may not be
        # positioned at the origin (0, 0), but the internal
        # data storage uses a 0 based list.
        #
        # To lookup data elements from pixel coordinates, they
        # must first be offset.
        self._pos = (float(position[0]), float(position[1]))

        # Maximum index coordinates along each axis.
        #
        # This value is exclusive, so bounds checks must use
        # less and not less-or-equal.
        self._dim = (int(dimensions[0]), dimensions[1])

        # Avoid divide-by-zero.
        if cell_size[0] <= 0.0 or cell_size[1] <= 0.0:
            raise ValueError("Cell size cannot be zero or less")

        # Cell size in pixels.
        self._cell_size = (float(cell_size[0]), float(cell_size[1]))

        # Each cell contains a set of bounding boxes it overlaps.
        #
        # An empty cell is represented by None.
        width, height = dimensions
        self._data = [None] * (width * height)  # type: List[Optional[Set[AABB2D]]]

    def cells_overlapped(self, aabb2d) -> Tuple[int, int]:
        """
        Helper to determine which cells the given bounding box overlaps.

        :param aabb2d: Target bounding box to test against.
        :return: Iterator of tuples containing cell indexes, 2D positions, and dimensions.
        """
        cell_w, cell_h = self._cell_size
        offset_x, offset_y = self._pos

        # Convert to integer required for ``range``
        x1, y1 = int(aabb2d.x - offset_x), int(aabb2d.y - offset_y)
        x2, y2 = x1 + int(aabb2d.width), y1 + int(aabb2d.height)

        # ``range`` semantics does the heavy lifting here
        for y in range(y1, y2, int(cell_h)):
            for x in range(x1, x2, int(cell_w)):
                i, j = int(floor(x / cell_w)), int(floor(y / cell_h))

                if self.index_in_bounds(i, j):
                    yield i, j

    def cell_contains(self, i, j, aabb2d):
        """
        Checks if the given bounding box is in the cell at the given coordinates.

        :param i:
        :param j:
        :param aabb2d: Bounding box.
        :return: True if the bounding box is in the cell.
        """
        return aabb2d in self._data[i + j * self._dim[0]]

    def insert(self, aabb2d):
        """
        Inserts a bounding box into the index.

        :param aabb2d: Bounding box.
        :return: Count of cells the bounding box was inserted into.
        """
        count = 0

        # Determine in which cells the bound box belongs
        for i, j in self.cells_overlapped(aabb2d):
            index = i + j * int(self._dim[0])

            cell = self._data[index]
            if cell is None:
                cell = set()
                self._data[index] = cell

            # Note set will deduplicate
            cell.add(aabb2d)

            count += 1

        return count

    def remove(self, aabb2d):
        """
        Removes the given bounding box from the index.

        The index must be up to date. If the bounding box has changed and is contained within the incorrect cells, then
        the removal will miss it.

        :param aabb2d: 2D axis aligned bounding box.
        """
        raise NotImplementedError()

    def recalculate(self):
        """
        Scans the entire index and moves bounding boxes between cells if their properties (position or size) has
        changed.
        """
        raise NotImplementedError()

    def find(self, query):
        """
        Queries the index for nearby neighbours.

        :param query: Either an aabb2d or a tuple with a 2D position.
        :return: Iterator over nearby neighbours.
        """
        if type(query) is tuple:
            # Position
            pass
        elif type(query) is AABB2D:
            # Bounding box
            pass
        else:
            raise TypeError("Grid spatial index cannot query using %s" % type(query).__name__)

        raise NotImplementedError()

    def index_in_bounds(self, i, j):
        m, n = self._dim
        return 0 <= i < m and 0 <= j < n
