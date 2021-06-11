import divHretention
import numpy as np
from pathlib import Path
import pytest


def test_exposition_ITER(tmpdir):
    """Test Exposition with ITER file
    """
    # build
    d = tmpdir.mkdir("test_data")

    filename = str(Path(d)) + "/example_ITER.csv"
    arc_length = np.linspace(0, 1)
    Te = np.linspace(1, 2)
    Ti = np.linspace(2, 3)
    D_temp_atm = np.linspace(3, 4)
    D_flux_atm = np.linspace(4, 5)
    D_flux_ion = np.linspace(5, 6)
    Wtot = np.linspace(6, 7)
    header = "x,Te,Ti,D_temp_atm,D_flux_ion,D_flux_atm,Wtot"
    data = np.asarray([arc_length, Te, Ti, D_temp_atm, D_flux_ion, D_flux_atm, Wtot]).T
    np.savetxt(filename, data, delimiter=",", header=header)
    expected_data = np.genfromtxt(filename, delimiter=",", names=True)

    # run
    my_exposure = divHretention.Exposition(filename, "ITER")

    # test
    for col_head in header.split(','):
        assert my_exposure.data[col_head].all() == expected_data[col_head].all()

    assert np.array_equal(my_exposure.arc_length, arc_length)
    assert np.array_equal(my_exposure.E_ion, 3*Te + 2*Ti)
    assert np.array_equal(my_exposure.E_atom, D_temp_atm)
    assert np.array_equal(my_exposure.atom_flux, D_flux_atm)
    assert np.array_equal(my_exposure.ion_flux, D_flux_ion)
    assert np.array_equal(my_exposure.net_heat_flux, Wtot)
    assert np.array_equal(my_exposure.angles_ions, np.ones(arc_length.shape)*60)
    assert np.array_equal(my_exposure.angles_atoms, np.ones(arc_length.shape)*45)


def test_exposition_WEST(tmpdir):
    """Test Exposition with WEST file
    """
    # build
    d = tmpdir.mkdir("test_data")

    filename = str(Path(d)) + "/example_WEST.csv"
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
    expected_data = np.genfromtxt(filename, delimiter=";", names=True)

    # run
    my_exposure = divHretention.Exposition(filename, "WEST")

    # test
    for col_head in header.split(';'):
        assert my_exposure.data[col_head].all() == expected_data[col_head].all()

    assert np.array_equal(my_exposure.arc_length, arc_length - 0.6)
    assert np.array_equal(my_exposure.E_ion, E_ions)
    assert np.array_equal(my_exposure.E_atom, E_atoms)
    assert np.array_equal(my_exposure.atom_flux, D_flux_atm)
    assert np.array_equal(my_exposure.ion_flux, D_flux_ion)
    assert np.array_equal(my_exposure.net_heat_flux, Wtot)
    assert np.array_equal(my_exposure.angles_ions, angle_ions)
    assert np.array_equal(my_exposure.angles_atoms, angle_atoms)


def test_exposition_unknown_type(tmpdir):
    """Test Exposition with an unknown filetype and checks that an error is
    raised
    """
    # build
    types = [1, "foo", "iter", "west"]

    # run
    for filetype in types:
        with pytest.raises(ValueError):
            my_exposure = divHretention.Exposition("foo", filetype)


def test_process_file_WEST(tmpdir):
    # build
    d = tmpdir.mkdir("test_data")

    filename = str(Path(d)) + "/example_WEST.csv"
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

    # run
    out = divHretention.Exposition(filename, "WEST")
    out.compute_inventory()

    # test
    my_exposure = divHretention.Exposition(filename, "WEST")
    assert np.array_equal(out.temperature, 1.1e-4*my_exposure.net_heat_flux + 323)
    assert np.array_equal(out.arc_length, my_exposure.arc_length)
    expected_concentration = divHretention.compute_c_max(
        out.temperature,
        my_exposure.E_ion, my_exposure.E_atom,
        my_exposure.angles_ions, my_exposure.angles_atoms,
        my_exposure.ion_flux, my_exposure.atom_flux)
    assert np.array_equal(out.concentration, expected_concentration)
    expected_inventory, expected_sigma = divHretention.compute_inventory(
        out.temperature,
        out.concentration,
        divHretention.DEFAULT_TIME)
    assert np.array_equal(out.inventory, expected_inventory)
    assert np.array_equal(out.stdev_inv, expected_sigma)


def test_process_file_ITER(tmpdir):
    # build
    d = tmpdir.mkdir("test_data")

    filename = str(Path(d)) + "/example_ITER.csv"
    arc_length = np.linspace(0, 1)
    Te = np.linspace(1, 2)
    Ti = np.linspace(2, 3)
    D_temp_atm = np.linspace(3, 4)
    D_flux_atm = np.linspace(4, 5)
    D_flux_ion = np.linspace(5, 6)
    Wtot = np.linspace(6, 7)
    header = "x,Te,Ti,D_temp_atm,D_flux_ion,D_flux_atm,Wtot"
    data = np.asarray([arc_length, Te, Ti, D_temp_atm, D_flux_ion, D_flux_atm, Wtot]).T
    np.savetxt(filename, data, delimiter=",", header=header)

    # run
    out = divHretention.Exposition(filename, "ITER")
    out.compute_inventory()

    # test
    my_exposure = divHretention.Exposition(filename, "ITER")
    assert np.array_equal(out.temperature, 1.1e-4*my_exposure.net_heat_flux + 323)
    assert np.array_equal(out.arc_length, my_exposure.arc_length)
    expected_concentration = divHretention.compute_c_max(
        out.temperature,
        my_exposure.E_ion, my_exposure.E_atom,
        my_exposure.angles_ions, my_exposure.angles_atoms,
        my_exposure.ion_flux, my_exposure.atom_flux)
    assert np.array_equal(out.concentration, expected_concentration)
    expected_inventory, expected_sigma = divHretention.compute_inventory(
        out.temperature,
        out.concentration,
        divHretention.DEFAULT_TIME)
    assert np.array_equal(out.inventory, expected_inventory)
    assert np.array_equal(out.stdev_inv, expected_sigma)
