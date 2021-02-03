import matplotlib.pyplot as plt
from matplotlib import ticker
import numpy as np

from main import process_file, extract_data


class plot_T_c_inv_along_divertor():
    def __init__(
            self, filenames=[], figsize=(8, 8), **kwargs):

        self.fig, self.axs = \
            plt.subplots(
                figsize=figsize, nrows=3,
                ncols=1, sharex="col", **kwargs)
        self.count = 0
        self.filenames = []

        plt.sca(self.axs[0])
        plt.ylabel(r"$c_\mathrm{surface}$ (m$^{-3}$)")
        plt.sca(self.axs[1])
        plt.ylabel(r"$T_\mathrm{surface}$ (K)")
        plt.sca(self.axs[2])
        plt.ylabel("Inventory per \n unit thickness \n (H/m)")
        plt.yscale("log")
        plt.xlabel("Distance along divertor (m)")
        for filename in filenames:
            self.add_case(filename)

    def add_case(self, filename):
        self.count += 1
        self.filenames.append(filename)

        label = "Case {}".format(self.count)
        res = process_file(filename)
        plt.sca(self.axs[0])
        plt.yscale("log")
        plt.plot(res.arc_length, res.concentration, label=label)
        plt.sca(self.axs[1])
        plt.plot(res.arc_length, res.temperature, label=label)
        plt.sca(self.axs[2])
        line, = plt.plot(res.arc_length, res.inventory, label=label)

        plt.fill_between(
            res.arc_length,
            10**(2*res.sigma_inv + np.log10(res.inventory)),
            10**(-2*res.sigma_inv + np.log10(res.inventory)),
            facecolor=line.get_color(), alpha=0.3)
        plt.legend()

    def show(self):
        plt.show()


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
        plt.ylabel("Incident flux")
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
