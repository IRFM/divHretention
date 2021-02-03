import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp2d
from inference.gp_tools import GpRegressor
from inference.gp_tools import RationalQuadratic, SquaredExponential

data = np.genfromtxt("data/data_TRIM_energy_angle.csv", delimiter=";", names=True)

# interpolate reflection coeff
sim_points = [[np.log10(E), theta] for E, theta in zip(data["Incident_energy"], data["theta_inc"])]
GP = GpRegressor(sim_points, data["Reflection_coeff"], kernel=RationalQuadratic)

# evaluate the estimate
Nx, Ny = 60, 5
gp_x = np.log10(np.logspace(1, np.log10(1400), Nx))
gp_y = np.linspace(0, 80, Ny)

gp_coords = [(i, j) for i in gp_x for j in gp_y]
mu_reflection, sig_reflection = GP(gp_coords)

reflection_coeff = interp2d(10**gp_x, gp_y, mu_reflection, kind='cubic')

# interpolate implantation range
sim_points = [[np.log10(E), theta] for E, theta in zip(data["Incident_energy"], data["theta_inc"])]
GP = GpRegressor(sim_points, data["Implantation_range"], kernel=RationalQuadratic)

# evaluate the estimate
Nx, Ny = 60, 5
gp_x = np.log10(np.logspace(1, np.log10(1400), Nx))
gp_y = np.linspace(0, 80, Ny)

gp_coords = [(i, j) for i in gp_x for j in gp_y]
mu_implantation_range, sig_implantation_range = GP(gp_coords)

implantation_range = interp2d(10**gp_x, gp_y, mu_implantation_range, kind='cubic')

if __name__ == '__main__':
    XX, YY = np.meshgrid(10**gp_x, gp_y)
    mu_mu = mu.reshape([Nx, Ny]).T
    sig_sig = sig.reshape([Nx, Ny]).T
    CS = plt.contourf(XX, YY, mu_mu, levels=1000)
    # CS = plt.contourf(XX, YY, sig_sig, levels=100)
    plt.scatter(data["Incident_energy"], data["theta_inc"], c=data["Reflection_coeff"], edgecolors="grey")
    plt.xlabel("Incident energy (eV)")
    plt.ylabel("Angle of incidence (°)")
    plt.xscale("log")
    plt.colorbar(CS, label="Reflection coefficient")
    plt.show()
