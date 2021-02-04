import matplotlib.pyplot as plt
from matplotlib import ticker
import numpy as np

from main import process_file, extract_data

correspondance_dict = {
    "arc_length": {
        "label": "Distance along divertor (m)"
    },
    "ion_energy": {
        "yscale": "log",
        "label": "Incident energy (eV)"
    },
    "atom_energy": {
        "yscale": "log",
        "label": "Incident energy (eV)"
    },
    "ion_flux": {
        "yscale": "log",
        "label": "Incident flux (m$^{-2}$ s^{-1}"
    },
    "atom_flux": {
        "yscale": "log",
        "label": "Incident flux (m$^{-2}$ s^{-1}"
    },
    "heat_flux": {
        "yscale": "log",
        "label": "Heat flux (W m$^{-2}$)"
    },
    "ion_angle": {
        "label": "Angle of incidence (°)"
    },
    "atom_angle": {
        "label": "Angle of incidence (°)"
    },
    "T_surf": {
        "label": r"$T_\mathrm{surface}$ (K)"
    },
    "c_surf": {
        "yscale": "log",
        "label": r"$c_\mathrm{surface}$ (m$^{-3}$)"
    },
    "inventory": {
        "yscale": "log",
        "label": "Inventory per \n unit thickness (H/m)"
    },
    "sigma_inv": {
    },
}


class plot_along_divertor():
    def __init__(
            self, filenames=[], quantities=["sigma_inv"],
            figsize=(8, 8), plot_sigma=True, **kwargs):

        self.fig, self.axs = \
            plt.subplots(
                figsize=figsize, nrows=len(quantities),
                ncols=1, sharex="col", **kwargs)
        self.count = 0
        self.filenames = []
        self.quantities = quantities
        self.plot_sigma = plot_sigma

        for filename in filenames:
            self.add_case(filename)

    def add_case(self, filename):
        self.count += 1
        self.filenames.append(filename)

        label = "Case {}".format(self.count)
        correspondance_dict = create_correspondance_dict(filename)
        arc_length = correspondance_dict["arc_length"]["var"]
        if len(self.quantities) == 1:
            axs = [self.axs]
        else:
            axs = self.axs
        for quantity, ax in zip(self.quantities, axs):
            if quantity not in correspondance_dict:
                raise ValueError(quantity + " is unknown")
            plt.sca(ax)
            if "yscale" in correspondance_dict[quantity]:
                plt.yscale(correspondance_dict[quantity]["yscale"])
            if "label" in correspondance_dict[quantity]:
                plt.ylabel(correspondance_dict[quantity]["label"])
            line, = plt.plot(
                arc_length, correspondance_dict[quantity]["var"])
            if quantity == "inventory" and self.plot_sigma:
                sigma = correspondance_dict["sigma_inv"]["var"]
                inventory = correspondance_dict[quantity]["var"]
                plt.fill_between(
                    arc_length,
                    10**(2*sigma + np.log10(inventory)),
                    10**(-2*sigma + np.log10(inventory)),
                    facecolor=line.get_color(), alpha=0.3)

        plt.legend()

    def show(self):
        plt.show()


def create_correspondance_dict(filename):
    R_div, Z_div, arc_length_div, E_ion_div, E_atom_div, ion_flux_div, \
        atom_flux_div, net_heat_flux_div, angles_ions, \
        angles_atoms, data = extract_data(filename)
    res = process_file(filename)
    correspondance_dict["arc_length"]["var"] = res.arc_length
    correspondance_dict["ion_energy"]["var"] = E_ion_div
    correspondance_dict["atom_energy"]["var"] = E_atom_div
    correspondance_dict["ion_flux"]["var"] = ion_flux_div
    correspondance_dict["atom_flux"]["var"] = atom_flux_div
    correspondance_dict["heat_flux"]["var"] = net_heat_flux_div
    correspondance_dict["ion_angle"]["var"] = angles_ions
    correspondance_dict["atom_angle"]["var"] = angles_atoms
    correspondance_dict["T_surf"]["var"] = res.temperature
    correspondance_dict["c_surf"]["var"] = res.concentration
    correspondance_dict["inventory"]["var"] = res.inventory
    correspondance_dict["sigma_inv"]["var"] = res.sigma_inv

    return correspondance_dict


class plot_T_c_inv_along_divertor(plot_along_divertor):
    def __init__(self, filenames=[], **kwargs):

        super().__init__(
            quantities=["T_surf", "c_surf", "inventory"],
            filenames=filenames,
            **kwargs)


# class plot_particle_exposure_along_divertor(plot_along_divertor):
#     def __init__(self, filenames=[], **kwargs):

#         super().__init__(
#             quantities=["T_surf", "c_surf", "inventory"],
#             filenames=filenames,
#             **kwargs)

class plot_particle_exposure_along_divertor():
    def __init__(
            self, filenames=[], figsize=(8, 8), **kwargs):

        self.fig, self.axs = \
            plt.subplots(
                figsize=figsize, nrows=3,
                ncols=1, sharex="col", **kwargs)
        self.count = 0
        self.filenames = []

        plt.sca(self.axs[0])
        plt.ylabel("Incident flux (H m$^{-2}$ s^{-1}")
        plt.yscale("log")
        plt.sca(self.axs[1])
        plt.ylabel("Incident energy (eV)")
        plt.yscale("log")
        plt.sca(self.axs[2])
        plt.ylabel("Angle of incidence (°)")
        plt.xlabel("Distance along divertor (m)")
        for filename in filenames:
            self.add_case(filename)

    def add_case(self, filename):
        self.count += 1
        self.filenames.append(filename)

        label = "Case {}".format(self.count)
        R_div, Z_div, arc_length_div, E_ion_div, E_atom_div, ion_flux_div, \
            atom_flux_div, net_heat_flux_div, angles_ions, \
            angles_atoms, data = extract_data(filename)

        # fluxes
        line, = self.axs[0].plot(arc_length_div, ion_flux_div, label=label)
        self.axs[0].plot(
            arc_length_div, atom_flux_div, label=label,
            color=line.get_color(), linestyle="dashed")
        # energy
        line, = self.axs[1].plot(arc_length_div, E_ion_div, label=label)
        self.axs[1].plot(
            arc_length_div, E_atom_div, label=label,
            color=line.get_color(), linestyle="dashed")
        # angle
        line, = self.axs[2].plot(arc_length_div, angles_ions, label=label)
        self.axs[2].plot(
            arc_length_div, angles_atoms, label=label,
            color=line.get_color(), linestyle="dashed")
        self.axs[2].legend()

    def show(self):
        plt.show()
