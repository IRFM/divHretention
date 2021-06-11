import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp2d
from inference.gp_tools import GpRegressor
from inference.gp_tools import RationalQuadratic, SquaredExponential

try:
    import importlib.resources as pkg_resources
except ImportError:
    # Try backported to PY<37 `importlib_resources`.
    import importlib_resources as pkg_resources

from . import data as data_module  # relative-import the *package* containing the templates


with pkg_resources.path(data_module, "data_TRIM_energy_angle.csv") as p:
    data = np.genfromtxt(p, delimiter=";", names=True)

step = 5
sim_points = [[np.log10(E), theta] for E, theta in zip(data["Incident_energy"][::step], data["theta_inc"][::step])]

# interpolate reflection coeff
GP_reflection_coeff = GpRegressor(sim_points, data["Reflection_coeff"][::step], kernel=RationalQuadratic)


def reflection_coeff(energy, angle):
    if energy == 0:
        return 0
    else:
        return GP_reflection_coeff((np.log10(energy), angle))[0]

# interpolate implantation range


def implantation_range(energy, angle):
    return 1.88e-10*energy**0.5924


if __name__ == '__main__':
    pass