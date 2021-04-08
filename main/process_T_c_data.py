import re
import os
from os import path

import numpy as np
import csv
from scipy.stats import linregress


def fit_powerlaw(x, y):
    slope, intercept, r_value, p_value, std_err = \
        linregress(np.log10(x), np.log10(y))
    a = 10**intercept
    b = slope
    return a, b


points = []
data = []

# extract high temp data
strings = []
folder = "data/monoblock_data/Solution_instantaneous_recomb_rand"
for f in os.listdir(folder):
    strings.append(os.path.join("/" + folder, f))

count = 0
for s in strings:
    match_number = re.compile('-?\ *[0-9]+\.?[0-9]*(?:[Ee]\ *-?\ *[0-9]+)?')
    e = re.findall(match_number, s)
    points.append([float(e[i])*10**float(e[i+1]) for i in [0, 2]])

    data.append({})
    data[-1]["T"] = points[-1][0]
    data[-1]["c"] = points[-1][1]
    filename = folder + "/T={:.2e};c={:.2e}/derived_quantities.csv".format(points[-1][0], points[-1][1])

    t = []
    inventory = []
    with open(filename, 'r') as csvfile:
        plots = csv.reader(csvfile, delimiter=',')
        next(plots)
        for row in plots:
            t.append(float(row[0]))
            inventory.append(
                2*(float(row[-1]) +
                    float(row[-2]) +
                    float(row[-3])))

    data[-1]["t"] = t
    data[-1]["inventory"] = inventory

# extract low temp data
L = 30e-3
strings = []
folder = "data/monoblock_data/Solution_instantaneous_recomb_low_temp"
for f in os.listdir(folder):
    strings.append(os.path.join("/" + folder, f))

for s in strings:
    match_number = re.compile('-?\ *[0-9]+\.?[0-9]*(?:[Ee]\ *-?\ *[0-9]+)?')
    e = re.findall(match_number, s)
    a = [float(e[i])*10**float(e[i+1]) for i in [0, 2]]
    if path.exists(folder + "/T={:.2e};c={:.2e}/derived_quantities.csv".format(a[0], a[1])):
        points.append(a)

        data.append({})
        data[-1]["T"] = points[-1][0]
        data[-1]["c"] = points[-1][1]

        filename = folder + "/T={:.2e};c={:.2e}/derived_quantities.csv".format(points[-1][0], points[-1][1])

        t = []
        inventory = []
        with open(filename, 'r') as csvfile:
            plots = csv.reader(csvfile, delimiter=',')
            next(plots)
            for row in plots:
                t.append(float(row[0]))
                inventory.append(
                    L*(float(row[-1]) +
                        float(row[-2]) +
                        float(row[-3])))
        a, b = fit_powerlaw(t, inventory)
        t_ = np.logspace(5, 7, num=100)
        inventory_ = a*t_**b
        data[-1]["t"] = t + t_.tolist()
        data[-1]["inventory"] = inventory + inventory_.tolist()

T_ = 320
for c in [*np.logspace(22 + np.log10(2), 23, num=7), *np.logspace(21 + np.log10(2), 22, num=7), *np.logspace(20 + np.log10(2), 21, num=7)]:
    points.append([T_, c])

    data.append({})
    data[-1]["T"] = T_
    data[-1]["c"] = c
    t = np.logspace(2, 7, num=100)
    D = 1.326e-10
    n = 6.93e25
    e = (t*2*D*c/n)**0.5
    inv = n*e*30e-3
    data[-1]["t"] = t
    data[-1]["inventory"] = inv


points = np.asarray(points)
# print(len(points), len(data))
