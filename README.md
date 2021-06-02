# divHretention

# Get started
```
pip install -r requirements.txt
```

Click [here](https://github.com/RemDelaporteMathurin/WEST-H-retention/blob/master/WEST_inventory.ipynb) for examples.

```python
import matplotlib.pyplot as plt
import numpy as np

from main import process_file
filenames = [
    "data/exposure_conditions_divertor/WEST/West-LSN-P1.6e+21-IP0.449MW.csv",
    "data/exposure_conditions_divertor/WEST/West-LSN-P2.5e+21-IP1.500MW.csv",
]

for i, filename in enumerate(filenames):
    res = process_file(filename)
    plt.plot(res.arc_length, res.inventory, label="Case {}".format(i+1))


plt.legend()
plt.xlabel("Distance along divertor (m)")
plt.ylabel("Inventory per unit thickness (H/m)")
plt.yscale("log")
plt.show()
```

![](/docs/example.png)
