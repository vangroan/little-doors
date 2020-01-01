from little_doors.aabb import AABB2D
from little_doors.grid import GridIndex2D


def test_cells_overlapped_simple():
    """
    Should return indexes of overlapped cells when grid is offset.
    """
    # assume
    grid = GridIndex2D(position=(-512.0, -512.0), dimensions=(32, 32), cell_size=(32.0, 32.0))

    # act
    indexes = grid.cells_overlapped(AABB2D(0.0, 0.0, 32.0, 32.0))

    # assert
    assert list(indexes) == [(16, 16)]


def test_cells_overlapped_negative_coord():
    """
    Should return indexes of overlapped cells of aabb2d in negative coordinates.
    """
    # assume
    grid = GridIndex2D(position=(-512.0, -512.0), dimensions=(32, 32), cell_size=(32.0, 32.0))

    # act
    indexes = grid.cells_overlapped(AABB2D(-64.0, -64.0, 64.0, 64.0))

    # assert
    assert list(indexes) == [(14, 14), (15, 14), (14, 15), (15, 15)]
