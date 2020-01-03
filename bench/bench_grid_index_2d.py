from timeit import timeit

from little_doors.aabb import AABB2D
from little_doors.grid import GridIndex2D

context = {
    'grid': GridIndex2D(),
}


def work():
    global context
    grid = context['grid']  # type: GridIndex2D
    aabb1 = AABB2D(0.0, 0.0, 32.0, 32.0)
    grid.insert(aabb1)
    aabb1.pos = 40.0, 40.0

    grid.recalculate()


if __name__ == '__main__':
    print(timeit(lambda: work(), number=60))
