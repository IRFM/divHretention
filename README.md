# divHretention

[![CircleCI](https://circleci.com/gh/IRFM/divHretention.svg?style=svg)](https://circleci.com/gh/IRFM/divHretention)
[![codecov](https://codecov.io/gh/IRFM/divHretention/branch/master/graph/badge.svg?token=WZVYJJHZ15)](https://codecov.io/gh/IRFM/divHretention)


divHretention is a tool to estimate ITER-like monoblock H inventories based on their surface temperature and surface concentration of H.

This package can be used to estimate H retention in tokamak divertors.

If you're using this package, please consider citing:

```
@article{delaporte-mathurin_parametric_2020,
	author = {Delaporte-Mathurin, Rémi and Hodille, Etienne and Mougenot, Jonathan and De Temmerman, Gregory and Charles, Yann and Grisolia, Christian},
	title = {Parametric study of hydrogenic inventory in the {ITER} divertor based on machine learning},
	journal = {Scientific Reports},
	volume = {10},
	number = {1},
	year = {2020},
	pages = {17798},
	doi = {10.1038/s41598-020-74844-w},
}
```

:point_right: [Documentation](https://divhretention.readthedocs.io/en/latest/)
:point_right: [Publication](https://doi.org/10.1038/s41598-020-74844-w)

# Get started
```
pip install divHretention
```

Click [here](https://divhretention.readthedocs.io/en/latest/WEST_inventory.html#Run-the-routine-from-files) for examples.


## Basic usage

```python
import matplotlib.pyplot as plt
import numpy as np
from divHretention import compute_inventory


x = np.linspace(0, 0.6, num=500)  # arc length (m) along the divertor
T = 320 + 1000*np.exp(-50*x)
concentration = 5e21*np.exp(-50*x)  # surface concentration (H m-3)

# compute the inventory (H/m) and standard deviation at 10 000s
inv, sig = compute_inventory(T, concentration, time=1e4)

plt.plot(x, inv)
plt.yscale("log")
plt.xlabel("Distance along divertor (m)")
plt.ylabel("Inventory per unit thickness (H/m)")
plt.show()
```
![](/docs/example_basic.png)

## From an input file

```python
import matplotlib.pyplot as plt

from divHretention import Exposition

filenames = [
    "examples/WEST/West-LSN-P1.6e+21-IP0.449MW.csv",
    "examples/WEST/West-LSN-P2.5e+21-IP1.500MW.csv",
]

for i, filename in enumerate(filenames):
    res = Exposition(filename, filetype="WEST")
    plt.plot(res.arc_length, res.inventory, label="Case {}".format(i+1))


plt.legend()
plt.xlabel("Distance along divertor (m)")
plt.ylabel("Inventory per unit thickness (H/m)")
plt.yscale("log")
plt.show()
```

![](/docs/example_files.png)
