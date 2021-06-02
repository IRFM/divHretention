"""
This script has to be executed at the root of the directory
"""
import re
import os
import matplotlib.pyplot as plt
import numpy as np
from main import plot_Tc_map_with_subplots


filenames = []
folder = "data/exposure_conditions_divertor/WEST/"
for f in os.listdir(folder):
    filenames.append(folder + str(f))

points = []
for filename in filenames:
    match_number = re.compile(r'-?\ *[0-9]+\.?[0-9]*(?:[Ee]\ *-?\ *[0-9]+)?')
    e = re.findall(match_number, filename)
    points.append(
        [float(e[0])*10**float(e[1]), float(e[2])]
        )
points = np.array(points)

plt.scatter(points[:, 0], points[:, 1])
plt.xlabel("Puffing Rate (s$^{-1}$)")
plt.ylabel("Input Power (MW)")
plt.show()

my_plot = plot_Tc_map_with_subplots(
    filenames=filenames,
    T_bounds=[320, 510],
    c_bounds=[1e20, 2e23])
plt.sca(my_plot.axs_bottom[1])
plt.show()
