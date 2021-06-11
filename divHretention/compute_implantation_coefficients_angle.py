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

from . import data as data_module


with pkg_resources.path(data_module, "data_TRIM_energy_angle.csv") as p:
    data = np.genfromtxt(p, delimiter=";", names=True)

step = 5
sim_points = [
    [np.log10(E), theta]
    for E, theta in
    zip(
        data["Incident_energy"][::step],
        data["theta_inc"][::step])]

# interpolate reflection coeff
GP_reflection_coeff = GpRegressor(
    sim_points, data["Reflection_coeff"][::step], kernel=RationalQuadratic)


def reflection_coeff(energy, angle):
    """Computes the reflection coefficient based on the particles incident
    energy and angle.

    Args:
        energy (float): incident energy in eV
        angle (float): angle of incidence in degree (0deg corresponds to a
            normal incidence)

    Returns:
        float: the reflection coefficient between 0 and 1. 1 = all particles
        are reflected, 0 = all particles are implanted
    """
    if energy == 0:
        return 0
    else:
        return GP_reflection_coeff((np.log10(energy), angle))[0]

# interpolate implantation range


def implantation_range(energy, angle):
    """Computes the reflection coefficient based on the particles incident
    energy and angle. Based on the formula:
    implantation range = 1.88e-10*energy^0.5924

    Args:
        energy (float): incident energy in eV
        angle (float): angle of incidence in degree (0deg corresponds to a
            normal incidence). Note: there is no angular dependence in this
            model

    Returns:
        float: the implantation range in m
    """
    return 1.88e-10*energy**0.5924


if __name__ == '__main__':
    pass
