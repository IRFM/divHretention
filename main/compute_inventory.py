import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import interp2d

from . import implantation_range, reflection_coeff
from . import extract_data
from . import estimate_inventory_with_gp_regression

inv, sig, points_x, points_y, sim_points = \
    estimate_inventory_with_gp_regression()

inv_T_c = interp2d(points_x, points_y, inv, kind='cubic')
sig_inv = interp2d(points_x, points_y, sig, kind='cubic')


def process_file(filename, inventory=True):
    R_div, Z_div, arc_length_div, E_ion_div, E_atom_div, ion_flux_div, \
        atom_flux_div, net_heat_flux_div, angles_ions, angles_atoms, data = \
        extract_data(filename)
    # Surface temperature from Delaporte-Mathurin et al, SREP 2020
    # https://www.nature.com/articles/s41598-020-74844-w
    T = 1.1e-4*net_heat_flux_div + 323

    # Compute the surface H concentration
    c_max = compute_c_max(T, E_ion_div, E_atom_div, angles_ions,
                          angles_atoms, ion_flux_div, atom_flux_div, filename)

    if inventory:
        # compute inventory as a function of temperature and concentration
        inventories, sigmas = compute_inventory(T, c_max)

    # output dict
    class Output:
        pass

    output = Output()
    output.arc_length = arc_length_div
    output.temperature = T
    output.concentration = c_max
    if inventory:
        output.inventory = inventories
        output.sigma_inv = sigmas

    return output


def compute_inventory(T, c_max):
    # compute inventory (H/m) along divertor
    e = 12e-3  # monoblock thickness (m)
    inventories = []  # inventory in H/m
    for temperature, concentration in zip(T, c_max):
        inventories.append(float(inv_T_c(temperature, concentration))/e)
    inventories = [
        float(inv_T_c(T_, c)) for T_, c in zip(T, c_max)]
    sigmas = [
        float(sig_inv(T_, c)) for T_, c in zip(T, c_max)]
    inventories, sigmas = np.array(inventories), np.array(sigmas)
    inventories *= 1/e   # convert in H/m
    return inventories, sigmas


def compute_c_max(
        T, E_ion, E_atom, angles_ion, angles_atom,
        ion_flux, atom_flux, filename, full_export=False):
    # Diffusion coefficient Fernandez et al Acta Materialia (2015)
    # https://doi.org/10.1016/j.actamat.2015.04.052
    D_0_W = 1.9e-7
    E_D_W = 0.2
    k_B = 8.6e-5
    D = D_0_W*np.exp(-E_D_W/k_B/T)

    # implantation ranges
    implantation_range_ions = [
        float(implantation_range(energy, angle))
        for energy, angle in zip(E_ion, angles_ion)]
    implantation_range_atoms = [
        float(implantation_range(energy, angle))
        for energy, angle in zip(E_atom, angles_atom)]

    # reflection coefficients
    reflection_coeff_ions = [
        float(reflection_coeff(energy, angle))
        for energy, angle in zip(E_ion, angles_ion)]
    reflection_coeff_atoms = [
        float(reflection_coeff(energy, angle))
        for energy, angle in zip(E_atom, angles_atom)]

    reflection_coeff_ions = np.array(reflection_coeff_ions)
    reflection_coeff_atoms = np.array(reflection_coeff_atoms)

    # compute c_max
    c_max_ions = (1 - reflection_coeff_ions) * \
        ion_flux*implantation_range_ions/D
    c_max_atoms = (1 - reflection_coeff_atoms) * \
        atom_flux*implantation_range_atoms/D
    c_max = c_max_ions + c_max_atoms

    if full_export:
        return c_max, c_max_ions, c_max_atoms
    else:
        return c_max


if __name__ == "__main__":
    pass
