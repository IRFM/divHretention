# FESTIM-SOLEDGE3X coupling project

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
    "data/exposure_conditions_divertor/WEST/Hao/WEST_54903_GP1.0e21_IP0.5MW_wall_data.mat",
    "data/exposure_conditions_divertor/WEST/Hao/WEST_54903_GP1.0e21_IP0.449MW_wall_data.mat",
    "data/exposure_conditions_divertor/WEST/Hao/WEST_54903_GP1.3e21_IP0.449MW_wall_data.mat",
    "data/exposure_conditions_divertor/WEST/Hao/WEST_54903_GP3.6e21_IP2.5MW_wall_data.mat",
    "data/exposure_conditions_divertor/WEST/Julien/WPN54696-1.5MW-FESTIM_inputs.csv"
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
