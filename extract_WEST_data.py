from scipy.interpolate import interp1d
import matplotlib.pyplot as plt
from matplotlib.colors import to_rgb
import csv
import scipy.io as scio
import numpy as np

filename = "exposure_conditions_divertor/WEST/Hao/wall_data.mat"
if filename.endswith("mat"):
    data = scio.loadmat(filename)
    R = data['R_wall']
    Z = data['Z_wall']
    Eion = data['Eion']
    Eatom = data['Eatom']
    ion_flux = data['ion_flux']
    atom_flux = data['atom_flux']
    net_heat_flux = data['net_heat_flux']
    ind_target = data['ind_target']
elif filename.endswith(("txt", "csv")):
    data = np.genfromtxt(filename, delimiter=";", names=True)
    R = data["R_wallm"]
    E = data["EioneV"]
    Z = data["Z_wallm"]


# indexes =  np.where((R > 1.9) & (R < 2.4) & (Z < -0.5))
index_start = 37
index_stop = 194
R_div = R[index_start:index_stop]
Z_div = Z[index_start:index_stop]
E_ion_div = Eion[index_start:index_stop]
E_atom_div = Eatom[index_start:index_stop]
ion_flux_div = ion_flux[index_start:index_stop]
atom_flux_div = atom_flux[index_start:index_stop]
net_heat_flux_div = net_heat_flux[index_start:index_stop]
ind_target_div = ind_target[index_start:index_stop]

# arc length for a straight line
arc_length_div = ((R_div - R_div[0])**2 + (Z_div - Z_div[0])**2)**0.5

if __name__ == "__main__":
    plt.figure()
    plt.plot(R, Z)
    plt.xlabel("R (m)")
    plt.ylabel("Z (m)")
    plt.plot(R_div, Z_div, label="Divertor")
    plt.legend()

    plt.figure()
    plt.plot(arc_length_div, E_ion_div, label="Ions")
    plt.plot(arc_length_div, E_atom_div, label="Atoms")
    plt.xlabel("Position along divertor (m)")
    plt.ylabel("Particle energy (eV)")
    plt.legend()

    plt.figure()
    plt.plot(arc_length_div, ion_flux_div, label="Ions")
    plt.plot(arc_length_div, atom_flux_div, label="Atoms")
    plt.xlabel("Position along divertor (m)")
    plt.ylabel("Particle flux (H/m2/s)")
    plt.legend()

    plt.figure()
    plt.plot(arc_length_div, net_heat_flux_div)
    plt.ylabel("Heat flux (W/m2)")
    plt.xlabel("Position along divertor (m)")
    plt.tight_layout()

    plt.figure()
    plt.plot(arc_length_div, ind_target_div)
    plt.xlabel("Position along divertor (m)")
    plt.ylabel("Particle flux (H/m2/s)")
    plt.legend()
    plt.show()
