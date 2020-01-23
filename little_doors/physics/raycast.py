from collections.abc import Iterator
from math import floor, ceil
from sys import float_info
from typing import Tuple

from little_doors.physics import vector3


def cast_grid_ray(position, direction, max_steps=10000, include_start=True, cell_size=(1.0, 1.0, 1.0)) \
        -> Iterator:
    """
    Cast a ray through an implicit voxel volume.

    Each step yields information on how far the ray has traveled, which
    voxel cell is intersected, and what is the position in 3D space where
    the intersection occurred.

    :type position: Tuple[float, float, float]
    :type direction: Tuple[float, float, float]
    :param max_steps: Limit on the number of steps the
        ray cast may travel to prevent it from iterating infinitely.
    :param include_start: Include the starting voxel, which contains the
        position coordinate, in the iterator's output.
    :param cell_size: Dimensions of each cell in the grid.
    """
    # Ensure direction is unit vector.
    d = vector3.normalize(*direction)

    # Length that the ray has travelled.
    #
    # Separate value per axis, as we are along the ray
    # stepping between the edges of voxels.
    tx, ty, tz = 0.0, 0.0, 0.0

    # The length along the ray we need to travel to
    # cross a voxel border along a specific axis.
    #
    # When the direction is 0.0 along an axis, then
    # it is parallel, and the ray will never cross
    # the voxel's border.
    if direction[0] != 0.0:
        delta_x = abs(1.0 / direction[0])
    else:
        delta_x = float_info.max

    if direction[1] != 0.0:
        delta_y = abs(1.0 / direction[1])
    else:
        delta_y = float_info.max

    if direction[2] != 0.0:
        delta_z = abs(1.0 / direction[2])
    else:
        delta_z = float_info.max

    # Determine which direction we are stepping.
    #
    # Calculate initial lengths from origin
    # to first crossing of boundries.
    if direction[0] > 0.0:
        step_x, tx = 1, abs(ceil(position[0]) - position[0]) * delta_x
    else:
        step_x, tx = -1, abs(floor(position[0]) - position[0]) * delta_x

    if direction[1] > 0.0:
        step_y, ty = 1, abs(ceil(position[1]) - position[1]) * delta_y
    else:
        step_y, ty = -1, abs(floor(position[1]) - position[1]) * delta_y

    if direction[2] > 0.0:
        step_z, tz = 1, abs(ceil(position[2]) - position[2]) * delta_z
    else:
        step_z, tz = -1, abs(floor(position[2]) - position[2]) * delta_z

    # Current cell coordinate
    i, j, k = _position_to_cell(position[0], position[1], position[2], cell_size)

    # Internal counter for the iterator.
    count = 0

    # The starting voxel may be important for the calling
    # algorithm that is doing the ray cast.
    if include_start:
        yield 0.0, (i, j, k), position

    while count < max_steps:
        # Takes current state of shortest axis ray, advances state for
        # next iteration, then unaltered returns state.

        if tx < ty:
            if tx < tz:
                # X-axis
                info = tx, (i, j, k), vector3.add(position, vector3.multiply(direction, tx))
                tx += delta_x
                i += step_x
                yield info
            else:
                # Z-axis
                info = tz, (i, j, k), vector3.add(position, vector3.multiply(direction, tz))
                tz += delta_z
                k += step_z
                yield info
        elif ty < tz:
            if ty < tz:
                # Y-axis
                info = ty, (i, j, k), vector3.add(position, vector3.multiply(direction, ty))
                ty += delta_y
                j += step_y
                yield info
            else:
                # Z-axis
                info = tz, (i, j, k), vector3.add(position, vector3.multiply(direction, tz))
                tz += delta_z
                k += step_z
                yield info
        else:
            # Z-axis
            info = tz, (i, j, k), vector3.add(position, vector3.multiply(direction, tz))
            tz += delta_z
            k += step_z
            yield info

        count += 1


def _position_to_cell(x, y, z, cell_size) -> Tuple[int, int, int]:
    return int(floor(x / cell_size[0])), int(floor(y / cell_size[1])), int(floor(z / cell_size[2]))


# ----------
# -- Test --
# ----------

def test_raycast():
    raycast = cast_grid_ray((0.5, 0.5, 0.5), (0.0, 0.0, 1.0), max_steps=10)
    for ray_info in raycast:
        print(ray_info)
