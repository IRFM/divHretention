"""
This script has to be executed at the root of the directory
"""
from main import extract_data, process_file, compute_c_max, compute_inventory
from main import plot_along_divertor
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import cm
from matplotlib.colors import Normalize
from scipy.stats import linregress

plt.rc('text', usetex=True)
plt.rc('font', family='serif', size=12)

input_power = 0.449
Ps = [
    4.4e20,
    1.0e21,
    1.3e21,
    1.6e21,
    2.0e21,
    2.5e21,
    2.9e21,
    3.3e21,
    3.83e21,
    4.36e21,
    4.7e21,
]
colormap = cm.viridis
sm = plt.cm.ScalarMappable(cmap=colormap, norm=Normalize(vmin=min(Ps), vmax=max(Ps)))
colours = [colormap((P - min(Ps))/max(Ps)) for P in Ps]

filenames = ["data/exposure_conditions_divertor/WEST/West-LSN-P{:.1e}-IP{:.3}MW.csv".format(P, input_power) for P in Ps]

time = 1e7  # s
# #### plot inventory along divertor

my_plot = plot_along_divertor(
    filenames,
    quantities=["T_surf", "c_surf", "inventory"],
    colors=colours,
    figsize=(6, 5))

plt.tight_layout()
plt.colorbar(
    sm, label="Puff rate (s$^{-1}$)",
    ax=my_plot.axs)
plt.savefig('Figures/WEST/inventory_along_divertor.pdf')
plt.savefig('Figures/WEST/inventory_along_divertor.svg')

# #### plot contribution ions along divertor
inventory_strike_point_inner = []
inventory_strike_point_outer = []
inventory_private_zone = []

sigma_strike_point_inner = []
sigma_strike_point_outer = []
sigma_private_zone = []

ratio_ions_inner_sp = []
ratio_ions_outer_sp = []
ratio_ions_private_zone = []

integrated_inventories = []
plt.figure()
for i, filename in enumerate(filenames):

    R, Z, arc_length, E_ion, E_atom, ion_flux, \
        atom_flux, net_heat_flux, angles_ion, angles_atom, data = \
        extract_data(filename)
    T = 1.1e-4*net_heat_flux + 323
    c_max, c_max_ions, c_max_atoms = compute_c_max(
        T, E_ion, E_atom, angles_ion, angles_atom,
        ion_flux, atom_flux, full_export=True)
    inventories, sigmas = compute_inventory(T, c_max, time=time)
    integrated_inventories.append(np.trapz(inventories, arc_length))

    line, = plt.plot(arc_length, c_max_ions/c_max, color=colours[i])

    inner_sp_loc_index = np.where(np.abs(arc_length-0.20) < 0.005)[0][0]
    outer_sp_loc_index = np.where(np.abs(arc_length-0.36) < 0.005)[0][0]
    private_zone_sp_loc_index = np.where(np.abs(arc_length-0.28) < 0.005)[0][0]

    inventory_strike_point_inner.append(inventories[inner_sp_loc_index])
    inventory_strike_point_outer.append(inventories[outer_sp_loc_index])
    inventory_private_zone.append(inventories[private_zone_sp_loc_index])

    sigma_strike_point_inner.append(sigmas[inner_sp_loc_index])
    sigma_strike_point_outer.append(sigmas[outer_sp_loc_index])
    sigma_private_zone.append(sigmas[private_zone_sp_loc_index])

    ratio_ions_inner_sp.append(c_max_ions[inner_sp_loc_index]/c_max[inner_sp_loc_index])
    ratio_ions_outer_sp.append(c_max_ions[outer_sp_loc_index]/c_max[outer_sp_loc_index])
    ratio_ions_private_zone.append(c_max_ions[private_zone_sp_loc_index]/c_max[private_zone_sp_loc_index])

plt.colorbar(sm, label="Puff rate (s$^{-1}$)")
plt.ylim(0, 1)
plt.xlabel("Distance along divertor (m)")
plt.ylabel("c surface (ions) / c surface")
plt.savefig('Figures/WEST/ion_ratio_along_divertor.pdf')
plt.savefig('Figures/WEST/ion_ratio_along_divertor.svg')

# #### plot inventory vs puffing rate

res = linregress(Ps, integrated_inventories)

puffin_rate_values = np.linspace(0.3e21, 5e21)

plt.figure(figsize=(6.4, 2.5))
line, = plt.plot(puffin_rate_values, res.intercept + puffin_rate_values*res.slope, linestyle="--")
plt.annotate(
    "{:.2f}".format(res.slope) + r"$\times p + $" + "{:.1e}".format(res.intercept),
    (3e21, 0.6e21),
    color=line.get_color())
plt.scatter(Ps, integrated_inventories, marker="+")
plt.xlabel("Puff rate (s$^{-1}$)")
plt.ylabel("Divertor H inventory (H)")
plt.ylim(bottom=0)
plt.xlim(left=0)
plt.tight_layout()
plt.savefig('Figures/WEST/inventory_vs_puffing_rate.pdf')
plt.savefig('Figures/WEST/inventory_vs_puffing_rate.svg')

# #### plot inventory at SPs and private zone
plt.figure(figsize=(6.4, 3))
line_spi, = plt.plot(Ps, inventory_strike_point_inner, marker="+", color="tab:blue")
line_spo, = plt.plot(Ps, inventory_strike_point_outer, marker="+", color="tab:blue")
line_pz,  = plt.plot(Ps, inventory_private_zone, marker="+", color="tab:orange")

sigma_strike_point_inner = np.array(sigma_strike_point_inner)
sigma_strike_point_outer = np.array(sigma_strike_point_outer)
sigma_private_zone = np.array(sigma_private_zone)

plt.fill_between(
    Ps,
    10**(2*sigma_strike_point_inner + np.log10(inventory_strike_point_inner)),
    10**(-2*sigma_strike_point_inner + np.log10(inventory_strike_point_inner)),
    facecolor=line_spi.get_color(), alpha=0.3)
plt.fill_between(
    Ps,
    10**(2*sigma_strike_point_outer + np.log10(inventory_strike_point_outer)),
    10**(-2*sigma_strike_point_outer + np.log10(inventory_strike_point_outer)),
    facecolor=line_spo.get_color(), alpha=0.3)
plt.fill_between(
    Ps,
    10**(2*sigma_private_zone + np.log10(inventory_private_zone)),
    10**(-2*sigma_private_zone + np.log10(inventory_private_zone)),
    facecolor=line_pz.get_color(), alpha=0.3)

plt.annotate("Inner strike point", (1.05*Ps[-1], inventory_strike_point_inner[-1]), color=line_spi.get_color())
plt.annotate("Outer strike point", (1.05*Ps[-1], inventory_strike_point_outer[-1]), color=line_spo.get_color())
plt.annotate("Private zone", (1.05*Ps[-1], inventory_private_zone[-1]), color=line_pz.get_color())
plt.xlim(right=1.4*Ps[-1])
plt.xlabel("Puff rate (s$^{-1}$)")
plt.ylabel("Inventory (H/m)")
plt.ylim(bottom=0)
plt.xlim(left=0)
plt.tight_layout()
plt.savefig('Figures/WEST/inventory_at_sp_and_private_zone.pdf')
plt.savefig('Figures/WEST/inventory_at_sp_and_private_zone.svg')

# #### plot ions vs atoms
fig, axs = plt.subplots(1, 3, sharey="row", sharex=True, figsize=(7, 3))
line_spi, = axs[0].plot(Ps, ratio_ions_inner_sp, marker="+", color="tab:blue")
axs[0].fill_between(
    Ps, np.zeros(len(Ps)), ratio_ions_inner_sp,
    facecolor='tab:blue', alpha=0.3)
axs[0].fill_between(
    Ps, np.zeros(len(Ps)) + 1, ratio_ions_inner_sp,
    facecolor='tab:orange', alpha=0.3)

line_spo, = axs[1].plot(Ps, ratio_ions_outer_sp, marker="+", color="tab:blue")
axs[1].fill_between(
    Ps, np.zeros(len(Ps)), ratio_ions_outer_sp,
    facecolor='tab:blue', alpha=0.3)
axs[1].fill_between(
    Ps, np.zeros(len(Ps)) + 1, ratio_ions_outer_sp,
    facecolor='tab:orange', alpha=0.3)

line_pz,  = axs[2].plot(Ps, ratio_ions_private_zone, marker="+", color="tab:orange")
axs[2].fill_between(
    Ps, np.zeros(len(Ps)), ratio_ions_private_zone,
    facecolor='tab:blue', alpha=0.3)
axs[2].fill_between(
    Ps, np.zeros(len(Ps)) + 1, ratio_ions_private_zone,
    facecolor='tab:orange', alpha=0.3)

axs[0].set_title("ISP", color=line_spi.get_color())
axs[1].set_title("OSP", color=line_spo.get_color())
axs[2].set_title("Private zone", color=line_pz.get_color())

axs[0].annotate("Ions", (3e21, 0.5), color="white", weight="bold")
axs[0].annotate("Atoms", (3.4e21, 0.6), color="white", weight="bold")
axs[1].annotate("Ions", (3e21, 0.4), color="white", weight="bold")
axs[1].annotate("Atoms", (3.4e21, 0.5), color="white", weight="bold")

# axs[2].annotate("Ions", (0.5e21, 0.1), color="white", weight="bold")
axs[2].annotate("Atoms", (1e21, 0.5), color="white", weight="bold")

plt.sca(axs[0])
plt.xlim(left=Ps[0], right=Ps[-1])
axs[0].set_xlabel("Puff rate (s$^{-1}$)")
axs[1].set_xlabel("Puff rate (s$^{-1}$)")
axs[2].set_xlabel("Puff rate (s$^{-1}$)")
plt.ylabel(r"$c_{\mathrm{surface}, \mathrm{ions}} / c_\mathrm{surface}$")
plt.ylim(bottom=0, top=1)
plt.yticks(ticks=[0, 0.5, 1])
# plt.xticks(ticks=[Ps[0], 2e21, Ps[-1]])
plt.tight_layout()
plt.savefig('Figures/WEST/ion_ratio_at_sp_and_private_zone.pdf')
plt.savefig('Figures/WEST/ion_ratio_at_sp_and_private_zone.svg')

plt.show()
