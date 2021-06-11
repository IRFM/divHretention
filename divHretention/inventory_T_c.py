import numpy as np
import scipy as sp
from scipy.interpolate import interp1d
from .process_T_c_data import points, data
from inference.gp_tools import GpRegressor
from inference.gp_tools import RationalQuadratic

import divHretention


def inv(points, time=1e7):
    ''' returns a 1D array'''
    values = []
    for p in points:
        for d in data:
            if d["T"] == p[0] and d["c"] == p[1]:
                values.append(interp1d(d["t"], d["inventory"])(time))
                break
    return np.asarray(values)


def estimate_inventory_with_gp_regression(time=1e7):
    """Estimate the monoblock inventory in H/m based on FESTIM results at a
    given time.

    The regression is made on T, log(c_surface), log(inventory)

    Args:
        time (float, optional): Exposure time in seconds. Defaults to 1e7.

    Returns:
        GpRegressor: callable, usage GP(600, np.log10(1e20)) see
        https://inference-tools.readthedocs.io/en/stable/GpRegressor.html
    """
    # with inference-tools
    sim_points = []
    z = []
    for p in points:
        if 320 <= p[0] <= 1100 and 1e20 <= p[1] <= 1e23:
            sim_points.append([p[0], np.log10(p[1])])
            z.append(np.log10(inv([p], time=time)))
    sim_points = np.array(sim_points)

    # Train the GP on the data
    GP = GpRegressor(
        sim_points[:: divHretention.step_mb],
        z[:: divHretention.step_mb],
        kernel=RationalQuadratic)

    # evaluate the estimate
    Nx, Ny = 50, 10
    gp_x = np.linspace(320, 1100, Nx)
    gp_y = np.log10(np.logspace(20, 23, Ny))
    gp_coords = [(i, j) for i in gp_x for j in gp_y]
    mu, sig = GP(gp_coords)

    return GP


if __name__ == "__main__":
    pass
