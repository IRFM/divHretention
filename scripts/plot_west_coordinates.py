import numpy as np
import matplotlib.pyplot as plt

data = np.genfromtxt("west_coordinates.csv", delimiter=",", names=True)

fw_x = data["first_wall_x"]
fw_y = data["first_wall_y"]
sep_x = data["primary_separatrix_x"]
sep_y = data["primary_separatrix_y"]


fig1, ax1 = plt.subplots()
ax1.set_aspect('equal')
plt.plot(fw_x, fw_y, color="tab:grey")
plt.plot(sep_x, sep_y, color="tab:grey", linestyle="dashed")

plt.xlabel("R(m)")
plt.ylabel("Z(m)")

plt.show()
