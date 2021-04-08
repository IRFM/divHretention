import numpy as np
import matplotlib.pyplot as plt

plt.rc('text', usetex=True)
plt.rc('font', family='serif', size=12)

fig1, axs = plt.subplots(ncols=2)

# ITER
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

plt.sca(axs[0])
axs[0].set_aspect('equal')
plt.plot(fw_x, fw_y, color="tab:grey")
plt.plot(div_x, div_y, color="tab:grey")
plt.plot(IVT_x, IVT_y, color="tab:red")
plt.plot(OVT_x, OVT_y, color="tab:red")
plt.plot(
    sep_x, sep_y, color="tab:grey",
    linestyle="dashed", label="Seperatrix")
plt.xlabel("R(m)")
plt.ylabel("Z(m)")

# WEST
data = np.genfromtxt("west_coordinates.csv", delimiter=",", names=True)

fw_x = data["first_wall_x"]
fw_y = data["first_wall_y"]
sep_x = data["primary_separatrix_x"]
sep_y = data["primary_separatrix_y"]
plt.sca(axs[0])
plt.plot(fw_x, fw_y, color="tab:grey")
plt.plot(sep_x, sep_y, color="tab:grey", linestyle="dashed")
plt.plot(fw_x[-12:-10], fw_y[-12:-10], color="tab:red", label="Targets")
plt.annotate('IVT', (3.5, -3), color="tab:red")
plt.annotate('OVT', (6, -4), color="tab:red")
plt.annotate('WEST', (2, 1.37), color="tab:grey")
plt.annotate('ITER', (4.7, 4.9), color="tab:grey")
plt.scatter(
    [4.1443, 5.56815], [-3.597, -4.283],
    facecolor='none', edgecolor="tab:red", label="Strike points", zorder=3)
plt.ylim(top=5.5)
plt.legend()

plt.sca(axs[1])
axs[1].yaxis.tick_right()
axs[1].yaxis.set_label_position("right")
axs[1].set_aspect('equal')
plt.plot(fw_x, fw_y, color="tab:grey")
plt.plot(sep_x, sep_y, color="tab:grey", linestyle="dashed")
plt.plot(fw_x[-12:-10], fw_y[-12:-10], color="tab:red")
plt.scatter(
    [2.146, 2.25255], [-0.678, -0.7205],
    facecolor='none', edgecolor="tab:red", zorder=3)
plt.annotate('WEST', (2.2, 0.85), color="tab:grey")
plt.ylim(top=1)

plt.xlabel("R(m)")
plt.ylabel("Z(m)")
plt.tight_layout()
plt.show()
