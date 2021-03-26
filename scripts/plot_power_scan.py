"""
This script has to be executed at the root of the directory
"""
from main import extract_data, process_file, compute_c_max, compute_inventory

from main import plot_along_divertor
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.colors import Normalize
import numpy as np
from scipy.stats import linregress


folder = "data/exposure_conditions_divertor/WEST/Hao/"
input_powers = [
    0.449,
    1,
    1.5,
    2
]
puff_rate = 2.5e21
filenames = [
    folder + "West-LSN-P{:.1e}-IP{:.3f}MW.csv".format(puff_rate, input_power)
    for input_power in input_powers]

colormap = cm.inferno
sm = plt.cm.ScalarMappable(cmap=colormap, norm=Normalize(vmin=min(input_powers), vmax=max(input_powers)))
colours = [colormap((IP - min(input_powers))/max(input_powers)) for IP in input_powers]

# inventory at SPs
my_plot = plot_along_divertor(
    filenames=filenames,
    quantities=["T_surf", "c_surf", "inventory"],
    figsize=(6, 5),
    colors=colours
)
plt.tight_layout()
plt.colorbar(
    sm, label="Input power (MW)",
    ax=my_plot.axs)
plt.savefig("Figures/WEST/inventory_along_divertor_input_power.pdf")
plt.savefig("Figures/WEST/inventory_along_divertor_input_power.svg")

# plot integrated inventory in divertor
plt.figure(figsize=(6.4, 2.5))
for puff_rate in [2.5e21, 4.44e21]:
    filenames = [
        folder + "West-LSN-P{:.1e}-IP{:.3f}MW.csv".format(puff_rate, input_power)
        for input_power in input_powers]

    inventories = []
    for filename in filenames:
        res = process_file(filename)
        inventory = np.trapz(res.inventory, res.arc_length)
        inventories.append(inventory)

    plt.scatter(
        input_powers, inventories, marker="+",
        label="{:.1e}".format(puff_rate) + " mol s$^{-1}$")
    res = linregress(input_powers, inventories)
    ip_values = np.linspace(input_powers[0], input_powers[-1])
    line, = plt.plot(
        ip_values, res.slope*ip_values + res.intercept,
        linestyle="--")
    plt.annotate(
        "{:.1e}".format(res.slope) + r"$\times IP + $" + "{:.1e}".format(res.intercept),
        (input_powers[-1] + 0.05, inventories[-1]),
        color=line.get_color()
    )
plt.xlim(left=0, right=input_powers[-1] + 1)
plt.ylim(bottom=0, top=1.8e21)
plt.xlabel("Input power (MW)")
plt.ylabel("Divertor H inventory (H)")
plt.legend(loc="lower right")
plt.tight_layout()
plt.savefig("Figures/WEST/inventory_vs_input_power.pdf")
plt.savefig("Figures/WEST/inventory_vs_input_power.svg")

# plot inventory at SPs
fig, axs = plt.subplots(1, 1, figsize=(6.4, 3), sharey=True, sharex=True)
labels = ["Inner strike point", "Outer strike point"]
linestyles = ["solid", "dashed"]
markers = ["+", "o"]
for i, puff_rate in enumerate([2.5e21, 4.44e21]):
    filenames = [
        folder + "West-LSN-P{:.1e}-IP{:.3f}MW.csv".format(puff_rate, input_power)
        for input_power in input_powers]
    inventories_inner_sp, sigmas_inner_sp = [], []
    inventories_outer_sp, sigmas_outer_sp = [], []
    inventories_pz, sigmas_pz = [], []

    for filename in filenames:
        res = process_file(filename)
        inner_sp_loc_index = np.where(np.abs(res.arc_length-0.20) < 0.005)[0][0]
        outer_sp_loc_index = np.where(np.abs(res.arc_length-0.36) < 0.005)[0][0]
        private_zone_sp_loc_index = np.where(np.abs(res.arc_length-0.28) < 0.005)[0][0]

        inventories_inner_sp.append(res.inventory[inner_sp_loc_index])
        inventories_outer_sp.append(res.inventory[outer_sp_loc_index])
        inventories_pz.append(res.inventory[private_zone_sp_loc_index])

        sigmas_inner_sp.append(res.sigma_inv[inner_sp_loc_index])
        sigmas_outer_sp.append(res.sigma_inv[outer_sp_loc_index])
        sigmas_pz.append(res.sigma_inv[private_zone_sp_loc_index])

    line_spi, = plt.plot(
        input_powers, inventories_inner_sp,
        label="{:.1e}".format(puff_rate) + " mol s$^{-1}$",
        marker=markers[i],
        color="tab:blue",
        linestyle=linestyles[i])
    line_spo, = plt.plot(
        input_powers, inventories_outer_sp,
        marker=markers[i],
        color="tab:blue",
        linestyle=linestyles[i])
    line_pz,  = plt.plot(
        input_powers, inventories_pz,
        marker=markers[i],
        color="tab:orange",
        linestyle=linestyles[i])

    if i == 1:
        plt.annotate("Inner strike point", (1.05*input_powers[-1], inventories_inner_sp[-1]), color=line_spi.get_color())
        plt.annotate("Outer strike point", (1.05*input_powers[-1], inventories_outer_sp[-1]), color=line_spo.get_color())
        plt.annotate("Private zone", (1.05*input_powers[-1], inventories_pz[-1]), color=line_pz.get_color())
plt.ylim(bottom=0, top=1e22)
plt.xlim(left=0, right=input_powers[-1] + 0.8)
plt.legend(loc="upper left")
plt.xlabel("Input power (MW)")
plt.ylabel("Divertor inventory (H)")
plt.tight_layout()

plt.savefig("Figures/WEST/inventory_at_sps_and_private_zone_vs_input_power.pdf")
plt.savefig("Figures/WEST/inventory_at_sps_and_private_zone_vs_input_power.svg")

plt.show()
