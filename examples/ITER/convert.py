"""
This script concatenates all the uncomplete .dat files and save the complete
data to .csv files.
Needs to be run for inner and outer targets (ie. _i and _o suffix respectively)
"""

import numpy as np
from numpy.lib.recfunctions import append_fields


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

for number in numbers:

    data1 = np.genfromtxt(
        "{}/ld_tg_o.dat".format(number),
        delimiter="\t", names=True, skip_header=18)
    data2 = np.genfromtxt(
        "{}/{}_fp_tg_o.dat".format(number, number),
        delimiter="\t", names=True, skip_header=11)

    for key in data2.dtype.names:
        if key not in ["x", "xMP", "f0"]:
            data1 = append_fields(data1, key, data2[key], np.double)
    np.savetxt(
        '{}/{}_outer_target.csv'.format(number, number), data1,
        delimiter=',', header=','.join(data1.dtype.names))
