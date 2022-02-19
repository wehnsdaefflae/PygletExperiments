# coding=utf-8
import math


def g(x: int) -> float:
    assert not (x < 0)
    if x == 0:
        return 0.
    return 1 / 2 ** math.ceil(math.log(x + 1, 2))


def h(x: int) -> int:
    assert not (x < 0)
    if x == 0:
        return 0
    return 2 ** math.ceil(math.log(x + 1, 2)) - x - 1


def spread_iterative(x: int) -> float:
    """
    Maximizes the distance between successive non-negative integers while minimizing total concentration on circumference of a circle.

    :param x: Input integer index.
    :return: Float from [0., 1.] indicating position on circumference of circle.
    """
    assert not (x < 0)
    if x == 0:
        return 0.
    s = 0.
    while x > 0:
        s += g(x)
        x = h(x - 1)
    return s
