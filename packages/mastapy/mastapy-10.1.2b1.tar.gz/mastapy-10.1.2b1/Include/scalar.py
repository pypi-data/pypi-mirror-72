import math
from typing import Union


NUM = Union[float, int]


def clamp(n: NUM, nmin: NUM, nmax: NUM) -> NUM:
    return min(nmax, max(nmin, n))


def sign(n: NUM) -> float:
    if n < 0.0:
        return -1.0
    elif n > 0.0:
        return 1.0
    else:
        return 0.0


def fract(n: float) -> float:
    return n - math.floor(n)


def step(edge: NUM, n: NUM) -> float:
    return 0.0 if edge > n else 1.0


def smoothstep(edge0: NUM, edge1: NUM, n: NUM) -> float:
    t = clamp((n - edge0) / (edge1 - edge0), 0.0, 1.0)
    return t * t * (3.0 - 2.0 * t)