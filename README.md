# divHretention

# Get started
```
pip install -r requirements.txt
```

Click [here](https://github.com/RemDelaporteMathurin/WEST-H-retention/blob/master/WEST_inventory.ipynb) for examples.


## Basic usage

```python
import matplotlib.pyplot as plt
import numpy as np
from main import compute_inventory

arc_length = np.linspace(0, 1)  # arc length (m) along the divertor
T = 1100*np.exp(-arc_length)  # temperature (K) profile
concentration = 1e20*np.exp(-arc_length)  # surface concentration (H m-3)

# compute the inventory (H/m) and standard deviation at 10 000s
inv, sig = compute_inventory(T, concentration, time=1e4)

plt.plot(arc_length, inv)
plt.xlabel("Distance along divertor (m)")
plt.ylabel("Inventory per unit thickness (H/m)")
plt.show()
```
![](/docs/example_basic.png)

## From an input file

```python
import matplotlib.pyplot as plt
import numpy as np

from main import process_file
filenames = [
    "data/exposure_conditions_divertor/WEST/West-LSN-P1.6e+21-IP0.449MW.csv",
    "data/exposure_conditions_divertor/WEST/West-LSN-P2.5e+21-IP1.500MW.csv",
]

for i, filename in enumerate(filenames):
    res = process_file(filename, filetype="WEST")
    plt.plot(res.arc_length, res.inventory, label="Case {}".format(i+1))


plt.legend()
plt.xlabel("Distance along divertor (m)")
plt.ylabel("Inventory per unit thickness (H/m)")
plt.yscale("log")
plt.show()
```

![](/docs/example_files.png)
