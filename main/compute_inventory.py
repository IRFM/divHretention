import matplotlib.pyplot as plt
import numpy as np

from . import implantation_range, reflection_coeff
from . import extract_data
from . import estimate_inventory_with_gp_regression

DEFAULT_TIME = 1e7

database_inv_sig = {}


def process_file(filename, filetype, inventory=True, time=DEFAULT_TIME):
    """Computes an output given a filename

    Args:
        filename (str): CSV file path. See extract_data.Exposition for
            information on the formatting.
        filetype (str): The type of CSV file "ITER" or "WEST".
        inventory (bool, optional): If True, the inventories and standard
            deviation will be computed and stored in the output. Defaults to
            True.
        time (float, optional): Time in seconds at which the inventory is
            computed. Defaults to 1e7.

    Returns:
        Output(): object with attributes "arc_length", "temperature",
            "concentration", "inventory", "sigma_inv"
    """
    # arc_length_div, E_ion_div, E_atom_div, ion_flux_div, \
    #     atom_flux_div, net_heat_flux_div, angles_ions, angles_atoms, data = \
    #     extract_data(filename)
    my_exposition = extract_data.Exposition(filename, filetype)
    # Surface temperature from Delaporte-Mathurin et al, SREP 2020
    # https://www.nature.com/articles/s41598-020-74844-w
    T = 1.1e-4*my_exposition.net_heat_flux + 323

    # Compute the surface H concentration
    c_max = compute_c_max(
        T,
        my_exposition.E_ion,
        my_exposition.E_atom,
        my_exposition.angles_ions,
        my_exposition.angles_atoms,
        my_exposition.ion_flux,
        my_exposition.atom_flux)

    if inventory:
        # compute inventory as a function of temperature and concentration
        inventories, sigmas = compute_inventory(T, c_max, time=time)

    # output dict
    class Output:
        pass

    output = Output()
    output.arc_length = my_exposition.arc_length
    output.temperature = T
    output.concentration = c_max
    if inventory:
        output.inventory = inventories
        output.sigma_inv = sigmas

    return output


def compute_inventory(T, c_max, time):
    """Computes the monoblock inventory as a function of the surface
    temperature, surface concentration and exposure time.
    If the time is not already in database_inv_sig, another gaussian
    regression is performed.

    Args:
        T (list): Surface temperature (K)
        c_max (list): Surface concentration (H m-3)
        time (float): Exposure time (s)

    Returns:
        numpy.array, numpy.array: list of inventories (H/m), list of standard
            deviation
    """
    if time not in database_inv_sig.keys():  # if time is not in the database
        GP = estimate_inventory_with_gp_regression(time=time)

        def inv_T_c_local(T, c):
            if c == 0:
                val = 0
            else:
                val = 10**GP((T, np.log10(c)))[0][0]
            return val

        def sig_inv_local(T, c):
            if c == 0:
                val = 0
            else:
                val = GP((T, np.log10(c)))[1][0]
            return val

        database_inv_sig[time] = {
            "inv": inv_T_c_local,
            "sig": sig_inv_local
        }
    else:
        inv_T_c_local = database_inv_sig[time]["inv"]
        sig_inv_local = database_inv_sig[time]["sig"]
    # compute inventory (H/m) along divertor
    inventories = [
        float(inv_T_c_local(T_, c)) for T_, c in zip(T, c_max)]
    sigmas = [
        float(sig_inv_local(T_, c)) for T_, c in zip(T, c_max)]
    inventories, sigmas = np.array(inventories), np.array(sigmas)
    return inventories, sigmas


def compute_c_max(
        T, E_ion, E_atom, angles_ion, angles_atom,
        ion_flux, atom_flux, full_export=False, isotope="H"):
    """Computes the surface concentration based on exposure conditions.

    Args:
        T (numpy.array): Surface temperature (K)
        E_ion (numpy.array): Ion incident energy (eV)
        E_atom (numpy.array): Atom incident energy (eV)
        angles_ion (numpy.array): Angle of incidence of ions (deg)
        angles_atom (numpy.array): Angle of incidence of atoms (deg)
        ion_flux (numpy.array): Ion flux (m-2 s-1)
        atom_flux (numpy.array): Atom flux (m-2 s-1)
        full_export (bool, optional): If True, the output will contain the
            surface concentration due to ions and atoms. Defaults to False.
        isotope (str, optional): Type of hydrogen isotope amongst "H", "D",
            "T". Defaults to "H".

    Returns:
        numpy.array or (numpy.array, numpy.array, numpy.array): surface
            concentration or (surface concentration, surface conc. ions,
            surface conc. atoms)
    """
    # Diffusion coefficient Fernandez et al Acta Materialia (2015)
    # https://doi.org/10.1016/j.actamat.2015.04.052
    D_0_W = 1.9e-7
    E_D_W = 0.2
    k_B = 8.617e-5
    D = D_0_W*np.exp(-E_D_W/k_B/T)
    if isotope == "D":
        D *= 1/2**0.5
    elif isotope == "T":
        D *= 1/3**0.5
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
