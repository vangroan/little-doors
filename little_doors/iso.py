"""
Isometric projection.
"""


def cart_to_iso(x, y, z):
    """
    Projects a 3D cartesian (x, y, z) coordinate to a 2D isometric (i, j, k) coordinate.

    >>> cart_to_iso(1, 1, 1)
    (0.0, 0.5, 1.0)

    >>> cart_to_iso(2, 3, 4)
    (0.0, 0.0, 4.0)

    >>> cart_to_iso(0, 2, 5)
    (0.0, 0.0, 5.0)
    """
    i = (float(x) - float(y)) * 0.5
    j = (float(y) + float(x)) * 0.25
    k = float(z)
    return i, j, k


def iso_to_cart():
    pass
