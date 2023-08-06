import numpy as np
import itertools
from scipy.interpolate import griddata

from .util import Envelope, norm_array

from typing import List, Tuple


_t_DEM = List[Tuple[float, float, float]]


class DEMObject:
    _dem: _t_DEM = None

    def __init__(self, dem: _t_DEM):
        self._dem = np.asarray(dem)

    def __repr__(self):
        return f"<DEMObject @ {len(self._dem)}>"

    def _axis(self, bound: Envelope, resolution: float):
        sx, sy = bound.west(), bound.south()
        ex, ey = bound.east(), bound.north()

        x_axis = np.arange(sx, ex+resolution, resolution)
        y_axis = np.arange(sy, ey+resolution, resolution)

        return x_axis, y_axis

    # 특정 해상도 (meter) 단위로 elevation grid 생성
    def grid(self, bound: Envelope, resolution: float=10.0):
        DEM = self._dem

        x_axis, y_axis = self._axis(bound, resolution)

        X, Y = np.meshgrid(x_axis, y_axis)
        Q = np.vstack([X.ravel(), Y.ravel()]).T
        # print(Q)

        Z = griddata((DEM[:, 0], DEM[:, 1]), DEM[:, 2], (Q[:, 0], Q[:, 1]), method='linear', fill_value=0)
        return np.vstack([Q[:, 0], Q[:, 1], Z]).T

    def slope(self, bound: Envelope, resolution: float=10.0):
        x_axis, y_axis = self._axis(bound, resolution)
        grid = self.grid(bound, resolution)

        height = grid[:,2]
        height = height.reshape((len(y_axis), len(x_axis)))

        grad_y, grad_x = np.gradient(height)

        vec_x = np.asarray([[resolution, 0.0, x] for x in list(itertools.chain(*grad_x))])
        vec_x = np.asarray(list(norm_array(vec_x)))
        vec_y = np.asarray([[0.0, resolution, y] for y in list(itertools.chain(*grad_y))])
        vec_y = np.asarray(list(norm_array(vec_y)))

        slope = np.cross(vec_x, vec_y)
        slope = np.asarray(list(norm_array(slope)))

        return np.hstack([grid, slope])
