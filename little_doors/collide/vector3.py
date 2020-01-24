from typing import Tuple
from math import sqrt


def add(a, b) -> Tuple[float, float, float]:
    """
    :type a: Tuple[float, float, float]
    :type b: Tuple[float, float, float]
    :param a:
    :param b:
    :return: Sum of the two given vectors.
    """
    return a[0] + b[0], a[1] + b[1], a[2] + b[2]


def subtract(a, b) -> Tuple[float, float, float]:
    """
    :type a: Tuple[float, float, float]
    :type b: Tuple[float, float, float]
    :param a:
    :param b:
    :return: Difference between the two given vectors.
    """
    return a[0] - b[0], a[1] - b[1], a[2] - b[2]


def multiply(v, s):
    """
    Multiply a vector with a scalar value.
    :param v: Tuple[float, float, float]
    :param s: float
    :return:
    """
    return v[0] * s, v[1] * s, v[2] * s


def magnitude(x, y, z):
    return sqrt(x ** 2 + y ** 2 + z ** 2)


def normalize(x, y, z):
    m = magnitude(x, y, z)
    if m == 0.0:
        return x, y, z
    return x / m, y / m, z / m
