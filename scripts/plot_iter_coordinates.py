import numpy as np
import matplotlib.pyplot as plt

data = np.genfromtxt("iter_coordinates.csv", delimiter=",", names=True)

div_x = data["divertor_x"]
div_y = data["divertor_y"]
IVT_x = div_x[:7]
IVT_y = div_y[:7]

OVT_x = div_x[-25:]
OVT_y = div_y[-25:]
fw_x = data["firstwall_x"]
fw_y = data["firstwall_y"]
sep_x = data["seperatrix_x"]
sep_y = data["seperatrix_y"]

fig1, ax1 = plt.subplots()
ax1.set_aspect('equal')
plt.plot(fw_x, fw_y, color="tab:grey")
plt.plot(div_x, div_y, color="tab:grey")
plt.plot(IVT_x, IVT_y, color="tab:red")
plt.plot(OVT_x, OVT_y, color="tab:red")
plt.plot(sep_x, sep_y, color="tab:grey", linestyle="dashed")

plt.xlabel("R(m)")
plt.ylabel("Z(m)")

plt.show()
