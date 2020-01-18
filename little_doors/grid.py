import itertools
from abc import ABC
from math import floor, ceil
from typing import Tuple, List, Optional, Set, Generator

from little_doors.aabb import AABB2D


class SpatialIndex2D(ABC):

    def find(self, query) -> Generator[Tuple[int, int, AABB2D], None, None]:
        raise NotImplementedError()


class GridIndex2D(SpatialIndex2D):
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

    def cells_overlapped(self, aabb2d) -> Generator[Tuple[int, int], None, None]:
        """
        Helper to determine which cells the given bounding box overlaps.

        :param aabb2d: Target bounding box to test against.
        :return: Generator yielding tuples containing cell indexes.
        """
        cell_w, cell_h = self._cell_size
        offset_x, offset_y = self._pos

        # Translate the bounding box's coordinates to the grid's coordinate for indexing.
        x1, y1 = aabb2d.x - offset_x, aabb2d.y - offset_y
        x2, y2 = x1 + aabb2d.width, y1 + aabb2d.height

        # Get index bounds for iteration.
        i_min, j_min = floor(x1 / cell_w), floor(y1 / cell_h)
        i_max, j_max = ceil(x2 / cell_w), ceil(y2 / cell_h)

        for j in range(int(j_min), int(j_max)):
            for i in range(int(i_min), int(i_max)):
                if self.index_in_bounds(i, j):
                    yield i, j

    def box_overlaps(self, i, j, aabb2d) -> bool:
        """
        Checks if the given bounding box overlaps with the given point.

        The bounding box does not need to have been inserted into in grid. This can be used
        to check whether a bounding box belongs in a cell or not.

        :type j: int
        :type i: int
        :type aabb2d: AABB2D
        :param i: Index coordinate along x-axis.
        :param j: Index coordinate along y-axis.
        :param aabb2d: Bounding box.
        :return: True if the bounding box overlaps the cell.
        """

        cell_w, cell_h = self._cell_size
        offset_x, offset_y = self._pos

        # Prepare an aabb2d-like tuple to leverage aabb2d overlap test
        x, y = offset_x + i * cell_w, offset_y + j * cell_h

        return aabb2d.overlap((x, y, cell_w, cell_h))

    def cell_contains(self, i, j, aabb2d):
        """
        Checks if the given bounding box is inside the cell bucket at the given coordinates.

        The bounding box must have been inserted into the grid for it to be contained.

        :param i: Index coordinate along x-axis.
        :param j: Index coordinate along y-axis.
        :param aabb2d: Bounding box.
        :return: True if the bounding box is in the cell.
        """
        cell = self._data[i + j * self._dim[0]]
        if cell is not None:
            return aabb2d in cell
        return False

    def insert(self, aabb2d) -> int:
        """
        Inserts a bounding box into the index.

        Importantly, a bounding box will not be inserted more than once into a cell. This
        method is safe to call multiple times.

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

    def remove(self, aabb2d) -> int:
        """
        Removes the given bounding box from the index.

        The index must be up to date. If the bounding box has changed and is contained within the incorrect cells, then
        the removal will miss it.

        :param aabb2d: 2D axis aligned bounding box.
        :return: Count of cells the aabb2d was removed from.
        """
        count = 0
        for i, j in self.cells_overlapped(aabb2d):
            if self._remove_coord(i, j, aabb2d):
                count += 1

        return count

    def _remove_coord(self, i, j, aabb2d):
        """
        Removes the given bounding box from the cell at coordinates i and j, regardless if
        the box's belongs there or not.

        :param i: Index coordinate along x-axis.
        :param j: Index coordinate along y-axis.
        :param aabb2d: Bounding box.
        :return: True if the cell contained the bounding box, false if it didnt.
        """

        index = i + j * self._dim[0]

        cell = self._data[index]
        if cell is not None:
            try:
                cell.remove(aabb2d)
                # Empty cells are None
                if not len(cell):
                    self._data[index] = None
                return True

            except KeyError:
                # Set does not contain element
                pass

        return False

    def purge(self, *aabb2ds) -> int:
        """
        An expensive remove operation that scans the whole grid to remove the given bounding box.

        :param aabb2ds: One or more bounding boxes to remove, in bulk.
        :return: Count of cells the aabb2d was removed from.
        """
        count = 0

        for cell in self._data:
            if cell is not None:
                for aabb in aabb2ds:
                    try:
                        cell.remove(aabb)
                        count += 1
                    except KeyError:
                        # Set does not contain element
                        pass

        return count

    def recalculate(self):
        """
        Scans the entire index and moves bounding boxes between cells if their properties (position or size) has
        changed.
        """
        # Mark inserts and removals to avoid mutating cell buckets during iteration.
        removals = []  # type: List[Tuple[int, int, AABB2D]]

        # Deduplicate inserts.
        #
        # Teh same bounding boxes may be mark for removal from
        # multiple cells. For the move operation, we only need
        # perform a single insert.
        inserts = set()

        width, height = self._dim

        for j in range(height):
            for i in range(width):
                index = i + j * width
                cell = self._data[index]
                if cell is not None:
                    for aabb2d in cell:
                        # Check if the current i and j overlap with this aabb2d.
                        if not self.box_overlaps(i, j, aabb2d):
                            # Bounding box does not belong in this cell, and probably
                            # needs to be inserted somewhere else.
                            removals.append((i, j, aabb2d))

                        # The box may need to be inserted somewhere else.
                        #
                        # Exclude testing the current i and j, since this is where
                        # we retrieved the box to begin with.
                        other = filter(lambda p: p != (i, j), self.cells_overlapped(aabb2d))
                        for k, l in other:
                            if self.box_overlaps(k, l, aabb2d) and not self.cell_contains(k, l, aabb2d):
                                inserts.add(aabb2d)

        for i, j, aabb2d in removals:
            self._remove_coord(i, j, aabb2d)

        for aabb2d in inserts:
            # Importantly the insert operation must deduplicate.
            self.insert(aabb2d)

    def find(self, query) -> Generator[Tuple[int, int, AABB2D], None, None]:
        """
        Queries the index for nearby neighbours.

        :type query: Union[AABB2D, Tuple[float, float]]
        :param query: Either an aabb2d or a tuple with a 2D position. When query is a tuple, the
            coordinates must be in pixels.
        :return: Generator yielding cell coordinates and nearby neighbours.
        """
        if type(query) is tuple:
            # Position
            raise NotImplementedError("Query by position not implemented yet")

        elif type(query) is AABB2D:
            # Bounding box
            for i, j in self.cells_overlapped(query):
                if self.index_in_bounds(i, j):
                    index = i + j * self._dim[0]
                    cell = self._data[index]
                    if cell is not None:
                        for aabb in cell:
                            yield i, j, aabb

        else:
            raise TypeError("Grid spatial index cannot query using %s" % type(query).__name__)

    def index_in_bounds(self, i, j):
        """
        Checks whether the given cell coordinates are inside the index's bounds.

        :return: True if within bounds.
        """
        m, n = self._dim
        return 0 <= i < m and 0 <= j < n


class IndexGroup2D(SpatialIndex2D):

    def __init__(self, first_index, *indexes):
        self._indexes = (first_index,) + indexes

    def find(self, query) -> Generator[object, None, None]:
        for n in itertools.chain(*(idx.find(query) for idx in self._indexes)):
            yield n
