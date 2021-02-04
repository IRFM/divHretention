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
        "label": "Incident energy (eV)",
        "linestyle": "solid"
    },
    "atom_energy": {
        "yscale": "log",
        "label": "Incident energy (eV)",
        "linestyle": "dashed"
    },
    "ion_flux": {
        "yscale": "log",
        "label": "Incident flux (m$^{-2}$ s^{-1}",
        "linestyle": "solid"
    },
    "atom_flux": {
        "yscale": "log",
        "label": "Incident flux (m$^{-2}$ s^{-1}",
        "linestyle": "dashed"
    },
    "heat_flux": {
        "yscale": "log",
        "label": "Heat flux (W m$^{-2}$)"
    },
    "ion_angle": {
        "label": "Angle of incidence (°)",
        "linestyle": "solid"
    },
    "atom_angle": {
        "label": "Angle of incidence (°)",
        "linestyle": "dashed"
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
            figsize=(8, 8), plot_sigma=True, overlap_ions_atoms=True,
            colors=None, **kwargs):

        self.count = 0
        self.filenames = []
        self.quantities = quantities
        self.plot_sigma = plot_sigma
        self.overlap_ions_atoms = overlap_ions_atoms
        self.nrows, self.axs_ids = self.compute_nrows()
        self.fig, self.axs = \
            plt.subplots(
                figsize=figsize, nrows=self.nrows,
                ncols=1, sharex="col", **kwargs)
        if colors is None:
            colors = plt.rcParams['axes.prop_cycle'].by_key()['color']
        for filename, color in zip(filenames, colors):
            self.add_case(filename, color)

    def compute_nrows(self):

        if not self.overlap_ions_atoms:
            N = len(self.quantities)
            axs_ids = [i for i in range(N)]
        else:
            N = 0
            axs_ids = []
            suffixes = {}
            for quantity in self.quantities:
                if quantity.endswith("_energy"):
                    if "_energy" not in suffixes:
                        suffixes["_energy"] = N
                        axs_ids.append(N)
                        N += 1
                    else:
                        axs_ids.append(suffixes["_energy"])
                        N += 0
                else:
                    axs_ids.append(N)
                    N += 1

        return N, axs_ids

    def add_case(self, filename, color):
        self.count += 1
        self.filenames.append(filename)

        label = "Case {}".format(self.count)
        correspondance_dict = create_correspondance_dict(filename)
        arc_length = correspondance_dict["arc_length"]["var"]
        if self.nrows == 1:
            axs = [self.axs]
        else:
            axs = self.axs
        for quantity, ax_id in zip(self.quantities, self.axs_ids):
            if quantity not in correspondance_dict:
                raise ValueError(quantity + " is unknown")
            plt.sca(axs[ax_id])
            if "yscale" in correspondance_dict[quantity]:
                plt.yscale(correspondance_dict[quantity]["yscale"])
            if "label" in correspondance_dict[quantity]:
                plt.ylabel(correspondance_dict[quantity]["label"])

            line, = plt.plot(
                arc_length, correspondance_dict[quantity]["var"],
                color=color)

            # use different linestyles if ions/atoms overlap
            if self.axs_ids.count(ax_id) > 1:
                line.set_linestyle(correspondance_dict[quantity]["linestyle"])

            # plot confidence interval
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
