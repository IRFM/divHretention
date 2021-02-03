from scipy.interpolate import interp1d
import matplotlib.pyplot as plt
from matplotlib.colors import to_rgb
import csv
import scipy.io as scio
import numpy as np


def extract_data(filename):
    arc_length_0 = 0.6  # this is the assumed beggining of the target
    if filename.endswith("mat"):
        data = scio.loadmat(filename)
        R = np.hstack(data['R_wall'])
        Z = np.hstack(data['Z_wall'])
        Eion = np.hstack(data['Eion'])
        Eatom = np.hstack(data['Eatom'])
        ion_flux = np.hstack(data['ion_flux'])
        atom_flux = np.hstack(data['atom_flux'])
        net_heat_flux = np.hstack(data['net_heat_flux'])
        ind_target = np.hstack(data['ind_target'])
        angles_ions = np.hstack(data["target_strike_angle"])
        angles_atoms = np.hstack(data["target_strike_angle"])  # TODO verify
        index_start = ind_target[0] - 1
        index_stop = ind_target[-1] - 1
        R_div = R[index_start:index_stop]
        Z_div = Z[index_start:index_stop]
        E_ion_div = Eion[index_start:index_stop]
        E_atom_div = Eatom[index_start:index_stop]
        ion_flux_div = ion_flux[index_start:index_stop]
        atom_flux_div = atom_flux[index_start:index_stop]
        net_heat_flux_div = net_heat_flux[index_start:index_stop]
        angles_ions = angles_ions[1:]
        angles_atoms = angles_atoms[1:]  # TODO: see why len(angles_atoms) != len(arc_length_div)

        # arc length for a straight line
        # arc_length_div = ((R_div - R_div[0])**2 + (Z_div - Z_div[0])**2)**0.5
        arc_length_div = np.hstack(data['length_wall'])
        arc_length_div = arc_length_div[index_start:index_stop]
        arc_length_div = arc_length_div - arc_length_0

    elif filename.endswith(("txt", "csv")):
        data = np.genfromtxt(filename, delimiter=";", names=True)
        R_div, Z_div = [], []
        arc_length_div = data["s_cell"] - arc_length_0
        E_ion_div = data["E_imp_ion"]
        E_atom_div = data["E_imp_atom"]
        angles_ions = data["alpha_V_ion"]
        angles_atoms = data["alpha_V_atom"]
        ion_flux_div = data["flux_imp_ion"]
        atom_flux_div = data["flux_imp_atom"]
        net_heat_flux_div = data["net_energy_flux"]

    return R_div, Z_div, arc_length_div, E_ion_div, E_atom_div, ion_flux_div, \
        atom_flux_div, net_heat_flux_div, angles_ions, angles_atoms, data


if __name__ == "__main__":
    filename = "data/exposure_conditions_divertor/WEST/Hao/P1.0e21_wall_data.mat"
    R_div, Z_div, arc_length_div, E_ion_div, E_atom_div, ion_flux_div, \
        atom_flux_div, net_heat_flux_div, data = extract_data(filename)
    plt.figure()
    plt.plot(data['R_wall'], data["Z_wall"])
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
    plt.show()
