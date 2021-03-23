"""
This script has to be executed at the root of the directory
"""
from main import extract_data, process_file, compute_c_max, compute_inventory
import matplotlib.pyplot as plt
import numpy as np

folder = "data/exposure_conditions_divertor/WEST/Hao/"
input_powers = [
    0.449,
    1,
    1.5,
    2
]

fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, sharex="col", sharey="row")

for puff_rate, axs in zip([2.5e21, 4.44e21], [(ax1, ax3), (ax2, ax4)]):

    for input_power in input_powers:
        filename = folder + \
            "West-LSN-P{:.1e}-IP{:.3f}MW.csv".format(puff_rate, input_power)
        R, Z, arc_length, E_ion, E_atom, ion_flux, \
            atom_flux, net_heat_flux, angles_ion, angles_atom, data = \
            extract_data(filename)
        T = 1.1e-4*net_heat_flux + 323
        c_max, c_max_ions, c_max_atoms = compute_c_max(
            T, E_ion, E_atom, angles_ion, angles_atom,
            ion_flux, atom_flux, filename, full_export=True)
        inventories, sigmas = compute_inventory(T, c_max)

        inventories_ions, sigmas_ions = compute_inventory(T, c_max_ions)

        plt.sca(axs[0])
        line, = plt.plot(
            arc_length,
            inventories,
            label="P = {:.1f} MW".format(input_power),
            alpha=0.8)

        plt.fill_between(
            arc_length,
            10**(2*sigmas + np.log10(inventories)),
            10**(-2*sigmas + np.log10(inventories)),
            facecolor=line.get_color(), alpha=0.2)

        plt.sca(axs[1])
        line, = plt.plot(
            arc_length,
            inventories_ions/inventories,
            label="P = {:.1f}".format(input_power), alpha=0.8)
    plt.sca(axs[0])
    plt.annotate("Puff rate: {:.1e}".format(puff_rate), (0, 1e22))

plt.sca(ax1)
plt.yscale("log")
plt.ylabel("Inventory per unit \n thickness (H/m)")

ax2.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.sca(ax3)
plt.xlabel("Distance along divertor (m)")
plt.ylabel("Inventory (ions) / Inventory")
plt.ylim(0, 1)
plt.sca(ax4)
plt.xlabel("Distance along divertor (m)")
plt.tight_layout()
plt.show()
