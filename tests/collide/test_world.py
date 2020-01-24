from little_doors.collide import PhysicsWorld3D


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