import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.colors import Normalize

from scipy.stats import linregress

from main import process_file

times = np.logspace(4, 7, num=5)
# fig, axs = plt.subplots(1, 2, sharey=True, figsize=(8, 3))
plt.figure()
folder = "data/exposure_conditions_divertor/ITER/"

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


# sort arrays
divertor_pressure = np.array(divertor_pressure)
numbers = np.array(numbers)
arr1inds = divertor_pressure.argsort()
numbers = numbers[arr1inds[::1]]
divertor_pressure = divertor_pressure[arr1inds[::1]]

colormap = cm.cividis
sm = plt.cm.ScalarMappable(cmap=colormap, norm=Normalize(vmin=min(divertor_pressure), vmax=max(divertor_pressure)))

filenames_inner = [
    "data/exposure_conditions_divertor/ITER/{}/{}_inner_target.csv".format(number, number) for number in numbers
    ]
filenames_outer = [
    "data/exposure_conditions_divertor/ITER/{}/{}_outer_target.csv".format(number, number) for number in numbers
    ]


as_, bs_ = [], []
for file_inner, file_outer, pressure in zip(filenames_inner, filenames_outer, divertor_pressure):
    inventories = []
    for time in times:
        inventory = 0
        for filename in [file_inner, file_outer]:
            res = process_file(filename, time=time)
            inventory += np.trapz(res.inventory, res.arc_length)
        inventories.append(inventory)
    plt.plot(times, inventories, marker="+", color=colormap((pressure - min(divertor_pressure))/max(divertor_pressure)))
    res = linregress(np.log10(times), np.log10(inventories))
    as_.append(10**res.intercept)
    bs_.append(res.slope)

plt.xscale("log")
plt.yscale("log")
plt.xlabel("Time (s)")
plt.ylabel("PFU inventory (H)")
plt.colorbar(sm, label="Divertor neutral pressure (Pa)")

# a, b
fig, axs = plt.subplots(2, 1, sharex="col")

axs[0].plot(divertor_pressure, as_, marker="+")
axs[1].plot(divertor_pressure, bs_, marker="+")


axs[0].set_ylabel("a")
axs[1].set_ylabel("b")
axs[1].set_xlabel("Divertor neutral pressure (Pa)")

axs[0].set_ylim(bottom=0)
axs[1].set_ylim(bottom=0)

axs[0].set_xlim(left=0)

plt.show()
