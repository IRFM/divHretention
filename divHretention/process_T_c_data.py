import re
import os
from os import path

import numpy as np
import csv
from scipy.stats import linregress

try:
    import importlib.resources as pkg_resources
except ImportError:
    # Try backported to PY<37 `importlib_resources`.
    import importlib_resources as pkg_resources
from divHretention import list_of_low_temp_files, list_of_high_temp_files
from .data import mb_high_temp
from .data import mb_low_temp


def fit_powerlaw(x, y):
    slope, intercept, r_value, p_value, std_err = \
        linregress(np.log10(x), np.log10(y))
    a = 10**intercept
    b = slope
    return a, b


points = []
data = []

# extract high temp data
strings = list_of_high_temp_files
count = 0
for s in strings:
    match_number = re.compile(r'-?\ *[0-9]+\.?[0-9]*(?:[Ee]\ *-?\ *[0-9]+)?')
    e = re.findall(match_number, s)
    points.append([float(e[i])*10**float(e[i+1]) for i in [0, 2]])

    data.append({})
    data[-1]["T"] = points[-1][0]
    data[-1]["c"] = points[-1][1]
    t = []
    inventory = []
    with pkg_resources.path(mb_high_temp, s) as file_path:
        with open(file_path, 'r') as csvfile:
            plots = csv.reader(csvfile, delimiter=',')
            next(plots)
            for row in plots:
                t.append(float(row[0]))
                inventory.append(
                    2*(float(row[-1]) +
                        float(row[-2]) +
                        float(row[-3])))
    # extrapolate to small times
    a, b = fit_powerlaw(t, inventory)
    t_ = np.logspace(2, 4, num=100)
    inventory_ = a*t_**b

    data[-1]["t"] = t_.tolist() + t
    data[-1]["inventory"] = inventory_.tolist() + inventory

# extract low temp data
L = 30e-3
strings = list_of_low_temp_files

for s in strings:
    match_number = re.compile(r'-?\ *[0-9]+\.?[0-9]*(?:[Ee]\ *-?\ *[0-9]+)?')
    e = re.findall(match_number, s)
    a = [float(e[i])*10**float(e[i+1]) for i in [0, 2]]
    points.append(a)

    data.append({})
    data[-1]["T"] = points[-1][0]
    data[-1]["c"] = points[-1][1]

    t = []
    inventory = []
    with pkg_resources.path(mb_low_temp, s) as file_path:
        with open(file_path, 'r') as csvfile:
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
    inv = n*e*L
    data[-1]["t"] = t
    data[-1]["inventory"] = inv


points = np.asarray(points)
# print(len(points), len(data))
