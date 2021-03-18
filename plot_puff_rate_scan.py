from main import extract_data, process_file, compute_c_max, compute_inventory
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import cm
from matplotlib.colors import Normalize

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

plt.figure(2)
colormap = cm.viridis
sm = plt.cm.ScalarMappable(cmap=colormap, norm=Normalize(vmin=min(Ps), vmax=max(Ps)))
plt.colorbar(sm, label="Puff rate (mol.s$^{-1}$)")

inventory_strike_point_inner = []
inventory_strike_point_outer = []
inventory_private_zone = []

ratio_ions_inner_sp = []
ratio_ions_outer_sp = []
ratio_ions_private_zone = []

for P in Ps:
    filename = "data/exposure_conditions_divertor/WEST/Hao/West-LSN-P{:.1e}-IP{:.3}MW.csv".format(P, input_power)
    R, Z, arc_length, E_ion, E_atom, ion_flux, \
        atom_flux, net_heat_flux, angles_ion, angles_atom, data = \
        extract_data(filename)
    T = 1.1e-4*net_heat_flux + 323
    c_max, c_max_ions, c_max_atoms = compute_c_max(
        T, E_ion, E_atom, angles_ion, angles_atom,
        ion_flux, atom_flux, filename, full_export=True)
    inventories, sigmas = compute_inventory(T, c_max)

    inventories_ions, sigmas_ions = compute_inventory(T, c_max_ions)
    inventories_atoms, sigmas_atoms = compute_inventory(T, c_max_atoms)

    plt.figure(1)
    line, = plt.plot(arc_length, inventories_ions/inventories, label="P = {:.1e}".format(P) + "mol.s$^{-1}$")

    plt.figure(2)
    line, = plt.plot(arc_length, inventories, label="P = {:.1e}".format(P), color=colormap((P - min(Ps))/max(Ps)))
    # plt.plot(arc_length, inventories_ions, linestyle="--", color=line.get_color())
    # plt.plot(arc_length, inventories_atoms, linestyle="-.", color=line.get_color())

    # plt.fill_between(
    #     arc_length, 10**(2*sigmas + np.log10(inventories)), 10**(-2*sigmas + np.log10(inventories)),
    #     facecolor=line.get_color(), alpha=0.3)

    inner_sp_loc_index = np.where(np.abs(arc_length-0.20) < 0.005)[0][0]
    outer_sp_loc_index = np.where(np.abs(arc_length-0.36) < 0.005)[0][0]
    private_zone_sp_loc_index = np.where(np.abs(arc_length-0.28) < 0.005)[0][0]

    inventory_strike_point_inner.append(inventories[inner_sp_loc_index])
    inventory_strike_point_outer.append(inventories[outer_sp_loc_index])
    inventory_private_zone.append(inventories[private_zone_sp_loc_index])

    ratio_ions_inner_sp.append(inventories_ions[inner_sp_loc_index]/inventories[inner_sp_loc_index])
    ratio_ions_outer_sp.append(inventories_ions[outer_sp_loc_index]/inventories[outer_sp_loc_index])
    ratio_ions_private_zone.append(inventories_ions[private_zone_sp_loc_index]/inventories[private_zone_sp_loc_index])


plt.figure(2)
plt.yscale("log")
plt.ylabel("Inventory per unit thickness (H/m)")
plt.xlabel("Distance along divertor (m)")
# plt.legend()

plt.figure(1)
plt.ylim(0, 1)
plt.xlabel("Distance along divertor (m)")
plt.ylabel("Inventory (ions) / Inventory")

plt.figure(3)
line_spi, = plt.plot(Ps, inventory_strike_point_inner, marker="+", color="tab:blue")
line_spo, = plt.plot(Ps, inventory_strike_point_outer, marker="+", color="tab:blue")
line_pz,  = plt.plot(Ps, inventory_private_zone, marker="+", color="tab:orange")

plt.annotate("Inner strike point", (1.05*Ps[-1], inventory_strike_point_inner[-1]), color=line_spi.get_color())
plt.annotate("Outer strike point", (1.05*Ps[-1], inventory_strike_point_outer[-1]), color=line_spo.get_color())
plt.annotate("Private zone", (1.05*Ps[-1], inventory_private_zone[-1]), color=line_pz.get_color())
plt.xlim(right=1.4*Ps[-1])
plt.xlabel("Puff rate (mol.s$^{-1}$)")
plt.ylabel("Inventory (H/m)")
plt.ylim(bottom=0)


# plot repartition ions/atoms
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

# plt.annotate("Inner strike point", (1.05*Ps[-1], ratio_ions_inner_sp[-1]), color=line_spi.get_color())
# plt.annotate("Outer strike point", (1.05*Ps[-1], ratio_ions_outer_sp[-1]), color=line_spo.get_color())
# plt.annotate("Private zone", (1.05*Ps[-1], ratio_ions_private_zone[-1]), color=line_pz.get_color())
axs[0].set_title("ISP")
axs[1].set_title("OSP")
axs[2].set_title("Private zone")

axs[0].annotate("Ions", (3e21, 0.7), color="white", weight="bold")
axs[0].annotate("Atoms", (3.4e21, 0.9), color="white", weight="bold")
axs[1].annotate("Ions", (3e21, 0.6), color="white", weight="bold")
axs[1].annotate("Atoms", (3.4e21, 0.9), color="white", weight="bold")

axs[2].annotate("Ions", (0.5e21, 0.1), color="white", weight="bold")
axs[2].annotate("Atoms", (1e21, 0.7), color="white", weight="bold")

plt.sca(axs[0])
plt.xlim(left=Ps[0], right=Ps[-1])
axs[0].set_xlabel("Puff rate \n (mol.s$^{-1}$)")
axs[1].set_xlabel("Puff rate \n (mol.s$^{-1}$)")
axs[2].set_xlabel("Puff rate \n (mol.s$^{-1}$)")
plt.ylabel("Inv (ions) / Inv")
plt.ylim(bottom=0, top=1)
plt.yticks(ticks=[0, 0.5, 1])
# plt.xticks(ticks=[Ps[0], 2e21, Ps[-1]])
plt.tight_layout()
plt.show()
