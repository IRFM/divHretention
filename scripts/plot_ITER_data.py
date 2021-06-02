"""
This script has to be executed at the root of the directory
"""

import re
import os
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.colors import Normalize

import numpy as np
from main import plot_Tc_map_with_subplots, plot_along_divertor, extract_data, compute_c_max, compute_inventory
import main
from scipy.interpolate import interp1d

plt.rc('text', usetex=True)
plt.rc('font', family='serif', size=12)

numbers = [
    2404,
    2403,
    2401,
    2402,
    2399,
    2400,
    2398,
    2397,
    2396,
]

divertor_pressure = [
    11.19639589,
    9.248295137,
    6.889631634,
    8.169794716,
    3.803158809,
    5.132170779,
    2.832874099,
    2.250856857,
    1.752557796,
]

time = 1e7  # s
# sort arrays
divertor_pressure = np.array(divertor_pressure)
numbers = np.array(numbers)
arr1inds = divertor_pressure.argsort()
numbers = numbers[arr1inds[::1]]
divertor_pressure = divertor_pressure[arr1inds[::1]]

colormap = cm.cividis
sm = plt.cm.ScalarMappable(cmap=colormap, norm=Normalize(vmin=min(divertor_pressure), vmax=max(divertor_pressure)))

colours = [colormap((P - min(divertor_pressure))/max(divertor_pressure)) for P in divertor_pressure]

filenames_inner = [
    "data/exposure_conditions_divertor/ITER/{}/{}_inner_target.csv".format(number, number) for number in numbers
    ]
filenames_outer = [
    "data/exposure_conditions_divertor/ITER/{}/{}_outer_target.csv".format(number, number) for number in numbers
    ]

res_inner, res_outer = [], []

for filename in filenames_inner:
    res = main.process_file(filename)
    res_inner.append(res)

for i, filename in enumerate(filenames_outer):
    res = main.process_file(filename)
    res_outer.append(res)

# compute total inventory
def integrate_inventory(res, x_max='max'):
    inventory_interp = interp1d(res.arc_length, res.inventory)
    if x_max == 'max':
        x_limit = res.arc_length.max()
    else:
        x_limit = x_max
    x_values = np.linspace(res.arc_length.min(), x_limit)
    inventory = np.trapz(inventory_interp(x_values), x_values)
    return inventory


def compute_total_inventory(x_max='max'):
    inventories_IVT, inventories_OVT = [], []
    for res in res_inner:
        inventory = integrate_inventory(res)
        inventories_IVT.append(inventory)
    for res in res_outer:
        inventory = integrate_inventory(res)
        inventories_OVT.append(inventory)
    return inventories_IVT, inventories_OVT


# ###### plot inventory vs divertor pressure
inventories_IVT, inventories_OVT = compute_total_inventory()
inventories = np.array(inventories_IVT) + np.array(inventories_OVT)
plt.figure()
line_tot, = plt.plot(divertor_pressure, inventories, marker="+", color="tab:brown")
line_inner, = plt.plot(divertor_pressure, inventories_IVT, marker="+", color="tab:red")
plt.fill_between(
    divertor_pressure, np.zeros(len(divertor_pressure)), inventories_IVT,
    alpha=0.3, color=line_inner.get_color())
plt.fill_between(
    divertor_pressure, inventories_IVT, inventories,
    alpha=0.3, color=line_tot.get_color())
plt.xlabel("Divertor neutral pressure (Pa)")
plt.ylabel("Divertor H inventory (H)")

plt.ylim(bottom=0)
plt.xlim(left=divertor_pressure[0], right=divertor_pressure[-1] + 1.5)
plt.annotate("IVT", (divertor_pressure[-1]+0.2, 0.4e22), color=line_inner.get_color(), weight="bold")
plt.annotate("OVT", (divertor_pressure[-1]+0.2, 0.6e22), color=line_tot.get_color(), weight="bold")
plt.savefig('Figures/ITER/inventory_vs_divertor_pressure.pdf')
plt.savefig('Figures/ITER/inventory_vs_divertor_pressure.svg')

# ###### plot exposure conditions along divertor

# my_plot = plot_Tc_map_with_subplots(
#     filenames=filenames_inner,
#     T_bounds=[320, 1200],
#     c_bounds=[1e20, 2e23])

# my_plot = plot_Tc_map_with_subplots(
#     filenames=filenames_outer,
#     T_bounds=[320, 1200],
#     c_bounds=[1e20, 2e23])
my_plot_inner = plot_along_divertor(
    filenames=filenames_inner,
    quantities=["T_surf", "c_surf", "inventory"],
    colors=colours,
    figsize=(6, 5))
plt.tight_layout()
my_plot_inner.axs[0].annotate("IVT", (0.5, 800))
plt.colorbar(
    sm, label="Divertor neutral pressure (Pa)",
    ax=my_plot_inner.axs)
plt.savefig('Figures/ITER/inventory_along_inner_divertor.pdf')
plt.savefig('Figures/ITER/inventory_along_inner_divertor.svg')

my_plot_outer = plot_along_divertor(
    filenames=filenames_outer,
    quantities=["T_surf", "c_surf", "inventory"],
    colors=colours,
    figsize=(6, 5))
plt.tight_layout()
my_plot_outer.axs[0].annotate("OVT", (0.5, 1500))
plt.colorbar(
    sm, label="Divertor neutral pressure (Pa)",
    ax=my_plot_outer.axs)
plt.savefig('Figures/ITER/inventory_along_outer_divertor.pdf')
plt.savefig('Figures/ITER/inventory_along_outer_divertor.svg')

# ###### compute inventory as function of x
fig, axs = plt.subplots(1, 2, sharey=True, figsize=(6.4, 3))
titles = ["IVT", "OVT"]
for i, results in enumerate([res_inner, res_outer]):
    plt.sca(axs[i])
    plt.title(titles[i])
    plt.xlabel("Distance along divertor (m)")
    for j, res in enumerate(results):
        inventories = []
        x_max_values = np.linspace(res.arc_length.min(), res.arc_length.max())
        for x_max in x_max_values:
            inventories.append(integrate_inventory(res, x_max=x_max))
        inventories = np.array(inventories)
        inventories *= 1/inventories.max()
        plt.plot(x_max_values, inventories, color=colours[j], alpha=0.8)

axs[0].set_ylabel("Cumulative inventory (norm.)")
plt.yticks(ticks=[0, 0.5, 1])
fig.colorbar(sm, label="Divertor neutral pressure (Pa)")
plt.tight_layout()
plt.subplots_adjust(wspace=0)
plt.ylim(0, 1)
plt.savefig('Figures/ITER/cumulative_inventory.pdf')
plt.savefig('Figures/ITER/cumulative_inventory.svg')

# ###### plot inventory at SPs
plt.figure(figsize=(6.4, 3))
labels = ["Inner strike point", "Outer strike point"]
for i, results in enumerate([res_inner, res_outer]):
    inventories, sigmas = [], []
    for res in results:
        sp_loc_index = np.where(res.temperature == res.temperature.max())[0][0]
        inventories.append(res.inventory[sp_loc_index])
        sigmas.append(res.sigma_inv[sp_loc_index])
    sigmas = np.array(sigmas)
    line, = plt.plot(divertor_pressure, inventories, label=labels[i], marker="+", color="tab:blue")
    plt.fill_between(
        divertor_pressure,
        10**(2*sigmas + np.log10(inventories)),
        10**(-2*sigmas + np.log10(inventories)),
        facecolor=line.get_color(), alpha=0.3)
    plt.annotate(labels[i], (1.05*divertor_pressure[-1], inventories[-1]), color=line.get_color())

plt.xlabel("Divertor neutral pressure (Pa)")
plt.ylabel("H inventory (H m$^{-1}$)")
plt.xlim(left=0, right=divertor_pressure[-1] + 4.5)
plt.ylim(bottom=0)
plt.tight_layout()
plt.savefig('Figures/ITER/inventory_at_strike_points.pdf')
plt.savefig('Figures/ITER/inventory_at_strike_points.svg')

# ###### plot neutral contribution
ratios = [[], []]
for i, results in enumerate([filenames_inner, filenames_outer]):
    for filename in results:
        R, Z, arc_length, E_ion, E_atom, ion_flux, \
            atom_flux, net_heat_flux, angles_ion, angles_atom, data = \
            extract_data(filename)
        T = 1.1e-4*net_heat_flux + 323
        c_max, c_max_ions, c_max_atoms = compute_c_max(
            T, E_ion, E_atom, angles_ion, angles_atom,
            ion_flux, atom_flux, full_export=True)

        inner_sp_loc_index = np.where(res.temperature == res.temperature.max())[0][0]

        ratios[i].append(c_max_ions[inner_sp_loc_index]/c_max[inner_sp_loc_index])

fig, axs = plt.subplots(1, 2, sharey="row", sharex=True, figsize=(5.5, 3))

ratio_ions_inner_sp = ratios[0]
line_spi, = axs[0].plot(divertor_pressure, ratio_ions_inner_sp, marker="+", color="tab:blue")
axs[0].fill_between(
    divertor_pressure, np.zeros(len(divertor_pressure)), ratio_ions_inner_sp,
    facecolor='tab:blue', alpha=0.3)
axs[0].fill_between(
    divertor_pressure, np.zeros(len(divertor_pressure)) + 1, ratio_ions_inner_sp,
    facecolor='tab:orange', alpha=0.3)

ratio_ions_outer_sp = ratios[1]
line_spo, = axs[1].plot(divertor_pressure, ratio_ions_outer_sp, marker="+", color="tab:blue")
axs[1].fill_between(
    divertor_pressure, np.zeros(len(divertor_pressure)), ratio_ions_outer_sp,
    facecolor='tab:blue', alpha=0.3)
axs[1].fill_between(
    divertor_pressure, np.zeros(len(divertor_pressure)) + 1, ratio_ions_outer_sp,
    facecolor='tab:orange', alpha=0.3)

axs[0].set_title("ISP")
axs[1].set_title("OSP")

axs[0].annotate("Ions", (3, 0.3), color="white", weight="bold")
axs[0].annotate("Atoms", (3.4, 0.5), color="white", weight="bold")
axs[1].annotate("Ions", (3.4, 0.55), color="white", weight="bold")
axs[1].annotate("Atoms", (5, 0.7), color="white", weight="bold")


plt.sca(axs[0])
plt.xlim(left=divertor_pressure[0], right=divertor_pressure[-1])
axs[0].set_xlabel("Divertor neutral pressure (Pa)")
axs[1].set_xlabel("Divertor neutral pressure (Pa)")
plt.ylabel(r"$c_{\mathrm{surface}, \mathrm{ions}} / c_\mathrm{surface}$")
plt.ylim(bottom=0, top=1)
plt.yticks(ticks=[0, 0.5, 1])
plt.tight_layout()
plt.savefig('Figures/ITER/ratio_ions_atoms.pdf')
plt.savefig('Figures/ITER/ratio_ions_atoms.svg')

plt.show()
