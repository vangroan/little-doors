from little_doors.aabb import AABB3D


def test_separation():
    # assume
    box1 = AABB3D(0.0, 0.0, 0.0, 1.0, 1.0, 1.0)
    box2 = AABB3D(1.0, 0.0, 0.0, 1.0, 1.0, 1.0)

    # act
    box_1_front_of_2 = box1.separation(box2)
    box_2_behind_1 = box2.separation(box1)

    # assert
    assert box_1_front_of_2 == (1, 0, 0)
    assert box_2_behind_1 == (-1, 0, 0)
