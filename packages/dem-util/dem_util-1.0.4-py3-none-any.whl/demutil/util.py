import numpy as np
import math
from typing import Tuple, Optional


_t_Point = Optional[Tuple[float, float]]


class Envelope:
    _east: float = None
    _west: float = None
    _north: float = None
    _south: float = None

    def __init__(self, nw: _t_Point=None, ne: _t_Point=None, sw: _t_Point=None, se: _t_Point=None, from_bound=None, from_shape=None):
        if from_bound is not None:
            self._west = from_bound[0]
            self._east = from_bound[2]
            self._south = from_bound[1]
            self._north = from_bound[3]

        elif from_shape is not None:
            bound = from_shape.bounds

            self._west = bound[0]
            self._east = bound[2]
            self._south = bound[1]
            self._north = bound[3]

        elif nw is not None:
            self._north = nw[1]
            self._west = nw[0]

            if se is not None:
                self._south = se[1]
                self._east = se[0]
            else:
                raise TypeError("must have south-east point")
        elif ne is not None:
            self._north = ne[1]
            self._east = ne[0]

            if sw is not None:
                self._south = sw[1]
                self._west = sw[0]
            else:
                raise TypeError("must have south-west point")
        else:
            raise TypeError("must have north-east or north-west point")

    def west(self) -> float:
        return self._west

    def east(self) -> float:
        return self._east

    def north(self) -> float:
        return self._north

    def south(self) -> float:
        return self._south


def norm_array(arr):
    for vec in arr:
        yield vec / np.linalg.norm(vec)


def vector_to_radian(vec):
    ref = np.asarray([0, 0, 1])

    return math.acos(np.dot(vec, ref) / np.linalg.norm(vec) * np.linalg.norm(ref))


def vector_to_bearing(vec):
    bearing = math.atan2(vec[0], vec[1])
    bearing = (bearing + (2*math.pi)) % (2*math.pi)

    return math.degrees(bearing)


def bearing_to_repr(bearing):
    val = int((bearing/22.5)+.5)
    arr = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE", "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"]

    return arr[(val % 16)]
