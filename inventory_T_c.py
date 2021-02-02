import numpy as np
import scipy as sp
from scipy.interpolate import griddata, interp2d, interp1d
import matplotlib.pyplot as plt
from matplotlib import ticker
from process_T_c_data import points, data
from inference.gp_tools import GpRegressor
from inference.gp_tools import RationalQuadratic, SquaredExponential

# try:
#     plt.rc('text', usetex=True)
#     plt.rc('font', family='serif', size=12)
# except:
#     pass


def scientificNotation(value):
    if value == 0:
        return '0'
    else:
        e = np.log10(np.abs(value))
        m = np.sign(value) * 10 ** (e - int(e))
        return r'${:.0f} \times 10^{{{:d}}}$'.format(m, int(e))


def inv(points, time=1e7):
    ''' returns a 1D array'''
    values = []
    for p in points:
        for d in data:
            if d["T"] == p[0] and d["c"] == p[1]:
                values.append(interp1d(d["t"], d["inventory"])(time))
                break
    return np.asarray(values)


# with inference-tools
e = 12e-3  # monoblock thickness (m)
points2 = []
z = []
for p in points:
    if 320 <= p[0] <= 1100 and 1e20 <= p[1] <= 1e23:
        points2.append([p[0], np.log10(p[1])])
        z.append(np.log10(e*inv([p], time=1e7)))
points2 = np.array(points2)

# Train the GP on the data
step = 3
GP = GpRegressor(points2[:: step], z[:: step], kernel=RationalQuadratic)


# evaluate the estimate
Nx, Ny = 50, 10
gp_x = np.linspace(320, 1100, Nx)
gp_y = np.log10(np.logspace(20, 23, Ny))
gp_coords = [(i, j) for i in gp_x for j in gp_y]
mu, sig = GP(gp_coords)

if __name__ == "__main__":

    # plot mu
    fig = plt.figure()
    locator = ticker.LogLocator(base=10)
    levels = np.logspace(
        min(mu),
        max(mu),
        1000)
    levels2 = np.logspace(
        min(mu),
        max(mu),
        10)
    # levels2 = np.delete(levels2, 4)
    CS = plt.contourf(*np.meshgrid(gp_x, 10**gp_y), 10**mu.reshape([Nx, Ny]).T, locator=locator, levels=levels)
    plt.colorbar(CS, label=r"Inventory per monoblock (H)", ticks=locator)
    CS2 = plt.contour(
        *np.meshgrid(gp_x, 10**gp_y), 10**mu.reshape([Nx, Ny]).T, levels=levels2,
        locator=locator, colors="white")
    manual_locations = [
        (861, 2e+20),
        (813, 3e+20),
        (781, 7e+20),
        (600, 7e+20),
        (1000, 3e+21),
        (1000, 5e+21),
        (431, 1e+22),
        (558, 2e+22)
        ]
    CLS = plt.clabel(CS2, inline=True, fontsize=10, fmt=scientificNotation, manual=manual_locations)
    plt.scatter(points2[:, 0], 10**np.array(points2[:, 1]), color=(0.5, 0.5, 0.5), alpha=0.3, marker="+")
    plt.yscale("log")
    plt.tick_params(axis='both', which='major', labelsize=13)
    plt.xlabel(r"$T_\mathrm{surface}$ (K)", fontsize=12)
    plt.ylabel(r"$c_\mathrm{surface}$ (m$^{-3}$)", fontsize=12)
    for c in CS.collections:  # for avoiding white lines in pdf
            c.set_edgecolor("face")
    plt.savefig("inv_with_points.svg")
    plt.show()