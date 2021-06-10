import time
import pytest
import numpy as np

import divHretention


def test_fecth_inventory_and_error():
    """Checks that fetch_inventory_and_error adds entries to database_inv_sig
    and that the execution time is smaller when fetching an already existing
    entry
    """
    # build
    for key in divHretention.database_inv_sig:
        # ensuring an empty database
        del divHretention.database_inv_sig[key]

    # test
    test_time = 1e3
    start_time = time.time()
    inv, sig = divHretention.fetch_inventory_and_error(test_time)
    long_time = time.time() - start_time

    start_time = time.time()
    inv, sig = divHretention.fetch_inventory_and_error(test_time)
    short_time = time.time() - start_time

    assert test_time in divHretention.database_inv_sig
    assert short_time < long_time


def test_compute_inventory():
    """Checks that compute_inventory runs correctly
    """
    T = [1000]
    c_max = [1e20]
    time = 1e3
    inv, sig = divHretention.compute_inventory(T, c_max, time)
    assert len(inv) == len(sig)
    assert len(inv) == len(T)


def test_compute_inventory_float():
    """Checks that compute_inventory raises a TypeError when a float is given
    """
    T = 1000
    c_max = 1e20
    time = 1e3
    with pytest.raises(TypeError):
        inv, sig = divHretention.compute_inventory(T, c_max, time)


def test_compute_c_max_h():
    """Runs compute_c_max with isotope H and checks that the correct value is
    produced
    """
    # build
    T = np.array([600, 500])
    E_ion = np.array([20, 10])
    E_atom = np.array([30, 40])
    angles_ion = np.array([60, 60])
    angles_atom = np.array([60, 60])
    ion_flux = np.array([1e21, 1e20])
    atom_flux = np.array([2e21, 2e20])

    # run
    c_max = divHretention.compute_c_max(
        T, E_ion, E_atom, angles_ion, angles_atom,
        ion_flux, atom_flux, full_export=False, isotope="H")

    # test
    D_0_W = 1.9e-7
    E_D_W = 0.2
    k_B = 8.617e-5
    D = D_0_W*np.exp(-E_D_W/k_B/T)

    # implantation ranges
    implantation_range_ions = [
        float(divHretention.implantation_range(energy, angle))
        for energy, angle in zip(E_ion, angles_ion)]
    implantation_range_atoms = [
        float(divHretention.implantation_range(energy, angle))
        for energy, angle in zip(E_atom, angles_atom)]

    # reflection coefficients
    reflection_coeff_ions = [
        float(divHretention.reflection_coeff(energy, angle))
        for energy, angle in zip(E_ion, angles_ion)]
    reflection_coeff_atoms = [
        float(divHretention.reflection_coeff(energy, angle))
        for energy, angle in zip(E_atom, angles_atom)]

    reflection_coeff_ions = np.array(reflection_coeff_ions)
    reflection_coeff_atoms = np.array(reflection_coeff_atoms)

    c_max_ions = (1 - reflection_coeff_ions) * \
        ion_flux*implantation_range_ions/D
    c_max_atoms = (1 - reflection_coeff_atoms) * \
        atom_flux*implantation_range_atoms/D
    c_max_expected = c_max_ions + c_max_atoms

    assert c_max.all() == c_max_expected.all()


def test_compute_c_max_D():
    """Runs compute_c_max with isotope D and checks that the correct value is
    produced
    """
    # build
    T = np.array([600, 500])
    E_ion = np.array([20, 10])
    E_atom = np.array([30, 40])
    angles_ion = np.array([60, 60])
    angles_atom = np.array([60, 60])
    ion_flux = np.array([1e21, 1e20])
    atom_flux = np.array([2e21, 2e20])

    # run
    c_max = divHretention.compute_c_max(
        T, E_ion, E_atom, angles_ion, angles_atom,
        ion_flux, atom_flux, full_export=False, isotope="D")

    # test
    D_0_W = 1.9e-7
    E_D_W = 0.2
    k_B = 8.617e-5
    D = D_0_W*np.exp(-E_D_W/k_B/T)
    D *= 1/2**0.5

    # implantation ranges
    implantation_range_ions = [
        float(divHretention.implantation_range(energy, angle))
        for energy, angle in zip(E_ion, angles_ion)]
    implantation_range_atoms = [
        float(divHretention.implantation_range(energy, angle))
        for energy, angle in zip(E_atom, angles_atom)]

    # reflection coefficients
    reflection_coeff_ions = [
        float(divHretention.reflection_coeff(energy, angle))
        for energy, angle in zip(E_ion, angles_ion)]
    reflection_coeff_atoms = [
        float(divHretention.reflection_coeff(energy, angle))
        for energy, angle in zip(E_atom, angles_atom)]

    reflection_coeff_ions = np.array(reflection_coeff_ions)
    reflection_coeff_atoms = np.array(reflection_coeff_atoms)

    c_max_ions = (1 - reflection_coeff_ions) * \
        ion_flux*implantation_range_ions/D
    c_max_atoms = (1 - reflection_coeff_atoms) * \
        atom_flux*implantation_range_atoms/D
    c_max_expected = c_max_ions + c_max_atoms

    assert c_max.all() == c_max_expected.all()


def test_compute_c_max_D():
    """Runs compute_c_max with isotope T and checks that the correct value is
    produced
    """
    # build
    T = np.array([600, 500])
    E_ion = np.array([20, 10])
    E_atom = np.array([30, 40])
    angles_ion = np.array([60, 60])
    angles_atom = np.array([60, 60])
    ion_flux = np.array([1e21, 1e20])
    atom_flux = np.array([2e21, 2e20])

    # run
    c_max = divHretention.compute_c_max(
        T, E_ion, E_atom, angles_ion, angles_atom,
        ion_flux, atom_flux, full_export=False, isotope="T")

    # test
    D_0_W = 1.9e-7
    E_D_W = 0.2
    k_B = 8.617e-5
    D = D_0_W*np.exp(-E_D_W/k_B/T)
    D *= 1/3**0.5

    # implantation ranges
    implantation_range_ions = [
        float(divHretention.implantation_range(energy, angle))
        for energy, angle in zip(E_ion, angles_ion)]
    implantation_range_atoms = [
        float(divHretention.implantation_range(energy, angle))
        for energy, angle in zip(E_atom, angles_atom)]

    # reflection coefficients
    reflection_coeff_ions = [
        float(divHretention.reflection_coeff(energy, angle))
        for energy, angle in zip(E_ion, angles_ion)]
    reflection_coeff_atoms = [
        float(divHretention.reflection_coeff(energy, angle))
        for energy, angle in zip(E_atom, angles_atom)]

    reflection_coeff_ions = np.array(reflection_coeff_ions)
    reflection_coeff_atoms = np.array(reflection_coeff_atoms)

    c_max_ions = (1 - reflection_coeff_ions) * \
        ion_flux*implantation_range_ions/D
    c_max_atoms = (1 - reflection_coeff_atoms) * \
        atom_flux*implantation_range_atoms/D
    c_max_expected = c_max_ions + c_max_atoms

    assert c_max.all() == c_max_expected.all()
    assert c_max.all() == c_max_expected.all()


def test_compute_c_max_output():
    """Runs compute_c_max and checks that the correct output
    """
    # build
    T = np.array([600, 500])
    E_ion = np.array([20, 10])
    E_atom = np.array([30, 40])
    angles_ion = np.array([60, 60])
    angles_atom = np.array([60, 60])
    ion_flux = np.array([1e21, 1e20])
    atom_flux = np.array([2e21, 2e20])

    # run
    output = divHretention.compute_c_max(
        T, E_ion, E_atom, angles_ion, angles_atom,
        ion_flux, atom_flux, full_export=True)

    # test
    assert len(output) == 3

    # run
    output = divHretention.compute_c_max(
        T, E_ion, E_atom, angles_ion, angles_atom,
        ion_flux, atom_flux, full_export=False)

    # test
    assert len(output) == 2
