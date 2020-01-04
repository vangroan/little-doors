"""
Vector math.
"""

from math import sqrt


def magnitude(x, y, z):
    return sqrt(x ** 2 + y ** 2 + z ** 2)


def normalize(x, y, z):
    m = magnitude(x, y, z)
    if m == 0.0:
        return x, y, z
    return x / m, y / m, z / m
