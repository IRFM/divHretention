from scipy.interpolate import interp1d
import matplotlib.pyplot as plt
from matplotlib.colors import to_rgb
import csv
import scipy.io as scio
import numpy as np


def extract_data(filename):
    arc_length_0 = 0.6  # this is the assumed beggining of the target

    data = np.genfromtxt(filename, delimiter=";", names=True)
    R_div, Z_div = [], []
    arc_length_div = data["s_cell_m"] - arc_length_0
    E_ion_div = data["E_imp_ion_eV"]
    E_atom_div = data["E_imp_atom_eV"]
    angles_ions = data["alpha_V_ion_deg"]
    angles_atoms = data["alpha_V_atom_deg"]
    ion_flux_div = data["flux_inc_ion_m2s1"]
    atom_flux_div = data["flux_inc_atom_m2s1"]
    net_heat_flux_div = data["net_energy_flux_Wm2"]

    # remove NaN in angles
    np.nan_to_num(angles_ions, copy=False, nan=60)
    np.nan_to_num(angles_atoms, copy=False, nan=45)

    # remove Nan in energy
    np.nan_to_num(E_ion_div, copy=False, nan=0.0)
    np.nan_to_num(E_atom_div, copy=False, nan=0.0)

    return R_div, Z_div, arc_length_div, E_ion_div, E_atom_div, ion_flux_div, \
        atom_flux_div, net_heat_flux_div, angles_ions, angles_atoms, data


if __name__ == "__main__":
    pass
