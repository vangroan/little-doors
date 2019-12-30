from little_doors.aabb import AABB3D
from little_doors.iso import hex_bounds


def test_hexagon_overlap():
    """
    Should test hexagons are overlapping.
    """
    # assume
    hex1 = hex_bounds(AABB3D(0.0, 0.0, 0.0, 1.0, 1.0, 1.0))
    hex2 = hex_bounds(AABB3D(1.0, 0.0, 0.0, 1.0, 1.0, 1.0))
    hex3 = hex_bounds(AABB3D(2.0, 0.0, 0.0, 1.0, 1.0, 1.0))

    # act
    hex_1_and_2 = hex1.overlaps(hex2)
    hex_2_and_3 = hex2.overlaps(hex3)
    hex_3_and_1 = hex3.overlaps(hex1)

    # assert
    assert hex_1_and_2
    assert hex_2_and_3
    assert not hex_3_and_1
