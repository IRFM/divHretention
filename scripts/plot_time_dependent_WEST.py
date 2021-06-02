import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.colors import Normalize

from scipy.stats import linregress

from main import process_file

times = np.logspace(5, 7, num=5)
fig, axs = plt.subplots(1, 2, sharey=True, figsize=(8, 3))
folder = "data/exposure_conditions_divertor/WEST/"
# puffing rate scan
plt.sca(axs[0])
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
colormap_puff_rate = cm.viridis
sm1 = plt.cm.ScalarMappable(cmap=colormap_puff_rate, norm=Normalize(vmin=min(Ps), vmax=max(Ps)))
as_puff_rate, bs_puff_rate = [], []
for P in Ps:
    filename = folder + "West-LSN-P{:.1e}-IP{:.3}MW.csv".format(P, input_power)
    inventories = []
    for time in times:
        res = process_file(filename, time=time)
        inventory = np.trapz(res.inventory, res.arc_length)
        inventories.append(inventory)
    plt.plot(times, inventories, marker="+", color=colormap_puff_rate((P - min(Ps))/max(Ps)))
    res = linregress(np.log10(times), np.log10(inventories))
    as_puff_rate.append(10**res.intercept)
    bs_puff_rate.append(res.slope)

plt.xscale("log")
plt.yscale("log")
plt.xlabel("Time (s)")
plt.ylabel("PFU inventory (H)")

# power scan
# plt.figure()
plt.sca(axs[1])

input_powers = [
    0.449,
    1,
    1.5,
    2
]
puff_rate = 4.44e21

colormap_ip = cm.inferno
sm2 = plt.cm.ScalarMappable(cmap=colormap_ip, norm=Normalize(vmin=min(input_powers), vmax=max(input_powers)))

as_input_power, bs_input_power = [], []
for IP in input_powers:
    filename = folder + \
                "West-LSN-P{:.1e}-IP{:.3f}MW.csv".format(puff_rate, IP)
    inventories = []
    for time in times:
        res = process_file(filename, time=time)
        inventory = np.trapz(res.inventory, res.arc_length)
        inventories.append(inventory)
    plt.plot(times, inventories, marker="+", color=colormap_ip((IP - min(input_powers))/max(input_powers)))
    res = linregress(np.log10(times), np.log10(inventories))
    as_input_power.append(10**res.intercept)
    bs_input_power.append(res.slope)
fig.colorbar(sm1, ax=axs[0], label="Puff rate (mol.s$^{-1}$)")
fig.colorbar(sm2, ax=axs[1], label="Input power (MW)")

plt.xscale("log")
plt.yscale("log")
plt.xlabel("Time (s)")
# plt.ylabel("PFU inventory (H)")
plt.tight_layout()

# plt.sca(axs[0])
# plt.annotate("IP = {:.2f} MW".format(input_power), (2e5, 1e21))
# plt.sca(axs[1])
# plt.annotate("PR = {:.1e} ".format(puff_rate) + "mol.s$^{-1}$", (2e5, 1e21))

fig, (ax_top, ax_bot) = plt.subplots(2, 2, sharey="row", sharex="col")

ax_top[0].plot(Ps, as_puff_rate, marker="+")
ax_bot[0].plot(Ps, bs_puff_rate, marker="+")

ax_top[1].plot(input_powers, as_input_power, marker="+")
ax_bot[1].plot(input_powers, bs_input_power, marker="+")

ax_top[0].set_ylabel("a")
ax_bot[0].set_ylabel("b")
ax_bot[0].set_xlabel("Puff rate (mol.s$^{-1}$)")
ax_bot[1].set_xlabel("Input power (MW)")

ax_top[0].set_ylim(bottom=0)
ax_bot[0].set_ylim(bottom=0)

ax_top[0].set_xlim(left=0)
ax_top[1].set_xlim(left=0)

plt.show()
