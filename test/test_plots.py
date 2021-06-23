import unittest
from pathlib import Path
import shutil
import tempfile
import pytest
import numpy as np

from divHretention import plot_Tc_map_with_subplots, \
    plot_T_c_inv_along_divertor, plot_inv_with_uncertainty, compute_inventory


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


def test_plot_inv_with_uncertainty():
    """
    Test for plot_inv_with_uncertainty
    """
    x = np.linspace(0, 0.6, num=500)  # arc length (m) along the divertor
    T = 350 + 1000*np.exp(-50*x)
    concentration = 7e21*(1 + np.exp(-50*x))  # surface concentration (H m-3)  
    zscore = 1
    inv, stdev = compute_inventory(T, concentration, time=1e3) 

    plot_inv_with_uncertainty(x, inv, stdev, zscore)


def test_plot_inv_with_uncertainty_type_error():
    """
    Test for plot_inv_with_uncertainty, when zscore is not a float
        - raise error
    """
    x = np.linspace(0, 0.6, num=500)  # arc length (m) along the divertor
    T = 350 + 1000*np.exp(-50*x)
    concentration = 7e21*(1 + np.exp(-50*x))  # surface concentration (H m-3)  

    inv, stdev = compute_inventory(T, concentration, time=1e3) 

    zscore_test = ['1', [1, 2, 3], np.array([1, 2, 3])]

    for test_value in zscore_test:
        zscore = test_value 

        with pytest.raises(TypeError,
                       match="zscore should be a float"):
            plot_inv_with_uncertainty(x, inv, stdev, zscore)
