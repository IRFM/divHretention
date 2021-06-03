import numpy as np


class Exposition:
    def __init__(self, filename):
        self.filename = filename
        self.arc_length = []
        self.E_ion = []
        self.E_atom = []
        self.ion_flux = []
        self.atom_flux = []
        self.net_heat_flux = []
        self.angles_ions = []
        self.angles_atoms = []
        self.data = None
        self.extract_data()
        self.remove_nan_values()

    def extract_data(self):
        """Extracts exposure data from a CSV file
        """
        if "ITER" in self.filename:
            self.extract_ITER_data(self.filename)
        elif "WEST" in self.filename:
            self.extract_WEST_data(self.filename)

    def extract_WEST_data(self, filename):
        self.data = np.genfromtxt(filename, delimiter=";", names=True)

        arc_length_0 = 0.6  # this is the assumed beggining of the target

        self.arc_length = self.data["s_cell_m"] - arc_length_0
        self.E_ion = self.data["E_imp_ion_eV"]
        self.E_atom = self.data["E_imp_atom_eV"]
        self.angles_ions = self.data["alpha_V_ion_deg"]
        self.angles_atoms = self.data["alpha_V_atom_deg"]
        self.ion_flux = self.data["flux_inc_ion_m2s1"]
        self.atom_flux = self.data["flux_inc_atom_m2s1"]
        self.net_heat_flux = self.data["net_energy_flux_Wm2"]

    def extract_ITER_data(self, filename):
        self.data = np.genfromtxt(filename, delimiter=",", names=True)
        self.arc_length = self.data["x"]
        self.E_ion = 3*self.data["Te"] + 2*self.data["Ti"]

        self.E_atom = self.data["D_temp_atm"]
        # angles not given
        default_angle_ion = 60
        default_angle_atom = 45
        self.angles_ions = np.ones(arc_length_0.shape)*default_angle_ion
        self.angles_atoms = np.ones(arc_length.shape)*default_angle_atom

        e = 1.6e-19  # C
        self.ion_flux = self.data["D_flux_ion"]
        self.atom_flux = self.data["D_flux_atm"]
        self.net_heat_flux = self.data["Wtot"]

    def remove_nan_values(self):
        # remove NaN in angles
        default_angle_ion = 60
        default_angle_atom = 45
        np.nan_to_num(self.angles_ions, copy=False, nan=default_angle_ion)
        np.nan_to_num(self.angles_atoms, copy=False, nan=default_angle_atom)

        # remove Nan in energy
        default_energy = 0.0
        np.nan_to_num(self.E_ion, copy=False, nan=default_energy)
        np.nan_to_num(self.E_atom, copy=False, nan=default_energy)


if __name__ == "__main__":
    pass
