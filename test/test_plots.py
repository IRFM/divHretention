import unittest
from pathlib import Path
import shutil
import tempfile
import pytest
import numpy as np

from divHretention import plot_Tc_map_with_subplots, \
    plot_T_c_inv_along_divertor


class TestExtrudeStraightShape(unittest.TestCase):
    def setUp(self):
        d = tempfile.mkdtemp("test_data")

        filename = str(Path(d)) + "/example_WEST.csv"
        self.filename = filename
        arc_length = np.linspace(0, 1)
        E_ions = np.linspace(1, 2)
        E_atoms = np.linspace(3, 4)
        angle_ions = np.linspace(4, 5)
        angle_atoms = np.linspace(5, 6)
        D_temp_atm = np.linspace(6, 7)
        D_flux_atm = np.linspace(7, 8)
        D_flux_ion = np.linspace(8, 9)
        Wtot = np.linspace(9, 10)
        header = "s_cell_m;E_imp_ion_eV;E_imp_atom_eV;alpha_V_ion_deg;alpha_V_atom_deg;flux_inc_ion_m2s1;flux_inc_atom_m2s1;net_energy_flux_Wm2"
        data = np.asarray([arc_length, E_ions, E_atoms, angle_ions, angle_atoms, D_flux_ion, D_flux_atm, Wtot]).T
        np.savetxt(filename, data, delimiter=";", header=header)

    def test_plot_2d_contour(self):
        plot_Tc_map_with_subplots(filenames=[self.filename, self.filename], filetypes="WEST")

    def test_plot_T_c_inv_along_div(self):
        plot_T_c_inv_along_divertor(filenames=[self.filename, self.filename], filetypes="WEST")
