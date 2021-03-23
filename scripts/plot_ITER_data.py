"""
This script has to be executed at the root of the directory
"""

import re
import os
import matplotlib.pyplot as plt
import numpy as np
from main import plot_Tc_map_with_subplots, plot_along_divertor
import main

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
numbers = numbers[arr1inds[::-1]]
divertor_pressure = divertor_pressure[arr1inds[::-1]]

inventories = []

filenames = ["data/exposure_conditions_divertor/ITER/Greg/{}/ld_tg_o.dat".format(number) for number in numbers]
for filename in filenames:
    res = main.process_file(filename)
    inventory = np.trapz(res.inventory, res.arc_length)
    inventories.append(inventory)

filenames = ["data/exposure_conditions_divertor/ITER/Greg/{}/ld_tg_i.dat".format(number) for number in numbers]
for i, filename in enumerate(filenames):
    res = main.process_file(filename)
    inventory = np.trapz(res.inventory, res.arc_length)
    inventories[i] += inventory


plt.plot(divertor_pressure, inventories, marker="+")
plt.xlabel("Divertor neutral pressure (Pa)")
plt.ylabel("Divertor H inventory (H.m$^{-1}$)")
plt.show()

my_plot = plot_Tc_map_with_subplots(
    filenames=filenames,
    T_bounds=[320, 1200],
    c_bounds=[1e20, 2e23])
plt.sca(my_plot.axs_bottom[1])
plt.show()
