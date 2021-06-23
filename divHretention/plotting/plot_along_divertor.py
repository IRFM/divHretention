import matplotlib.pyplot as plt
from matplotlib import ticker
import numpy as np

from divHretention import Exposition

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
        "label": "Incident flux (m$^{-2}$ s$^{-1}$)",
        "linestyle": "solid"
    },
    "atom_flux": {
        "yscale": "log",
        "label": "Incident flux (m$^{-2}$ s$^{-1}$)",
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
    "stdev_inv": {
    },
}


class plot_along_divertor():
    """Plots some quantities along the divertor arc length. This class works
    with csv files (see :func:`Exposition()
    <divHretention.extract_data.Exposition>`).

    Args:
        filenames (list, optional): The CSV file names. Defaults to [].
        filetypes (list or str, optional): The CSV file types
            ("WEST" or "ITER"). Defaults to [].
        quantities (list, optional): The quantities to be plotted
            (see :py:meth:`correspondance_dict` in
            :py:mod:`plot_along_divertor`). Defaults to ["stdev_inv"].
        figsize (tuple, optional): The size of the figure. Defaults to (8, 8).
        plot_sigma (bool, optional): If true, the 95% confidence interval will
            be plotted. Defaults to True.
        overlap_ions_atoms (bool, optional): If True, energies, fluxes and
            angles of ions and atoms will be plotted on the same plot.
            Defaults to True.
        colors (list, optional): List of matplotlib colors. The length of
            `colors` must be the same as `filetypes`. Defaults to None.

    Raises:
        ValueError: if missing the filetypes argument
    """
    def __init__(
            self, filenames=[], filetypes=[], quantities=["stdev_inv"],
            figsize=(8, 8), plot_sigma=True, overlap_ions_atoms=True,
            colors=None, **kwargs):

        self.count = 0
        self.filenames = []

        if len(filenames) > 0 and len(filetypes) == 0:
            raise ValueError("Missing filetypes argument")
        if type(filetypes) is str:
            self.filetypes = [filetypes for _ in filenames]
        else:
            self.filetypes = filetypes[:]
        self.quantities = quantities
        self.plot_sigma = plot_sigma
        self.overlap_ions_atoms = overlap_ions_atoms
        self.nrows, self.axs_ids = self.compute_nrows()
        self.fig, self.axs = \
            plt.subplots(
                figsize=figsize, nrows=self.nrows,
                ncols=1, sharex="col", **kwargs)
        self.axs[-1].set_xlabel("Distance along divertor (m)")
        if colors is None:
            colors = plt.rcParams['axes.prop_cycle'].by_key()['color']
        for filename, filetype, color in \
                zip(filenames, self.filetypes, colors):
            self.add_case(filename, filetype, color)

    def compute_nrows(self):
        """Compute the number of rows needed

        Returns:
            int, list: number of rows, list of axes
        """
        if not self.overlap_ions_atoms:
            N = len(self.quantities)
            axs_ids = [i for i in range(N)]
        else:
            N = 0
            axs_ids = []
            all_suffixes = ["_energy", "_angle", "_flux"]
            suffixes = {}
            for quantity in self.quantities:
                has_suffix = False
                for suffix in all_suffixes:
                    if quantity.endswith(suffix) and quantity != "heat_flux":
                        has_suffix = True
                        if suffix not in suffixes:
                            suffixes[suffix] = N
                            axs_ids.append(N)
                            N += 1
                        else:
                            axs_ids.append(suffixes[suffix])
                            N += 0

                if not has_suffix:
                    axs_ids.append(N)
                    N += 1

        return N, axs_ids

    def add_case(self, filename, filetype, color):
        """Adds a new exposure case to the plot.

        Args:
            filename (str): The CSV file name.
            filetype (str): The CSV file type
                ("WEST" or "ITER").
            color (str): the color of the line.

        Raises:
            ValueError: If a quantity is unknown.
        """
        self.count += 1
        self.filenames.append(filename)

        label = "Case {}".format(self.count)
        correspondance_dict = create_correspondance_dict(filename, filetype)
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
                sigma = correspondance_dict["stdev_inv"]["var"]
                inventory = correspondance_dict[quantity]["var"]
                plt.fill_between(
                    arc_length,
                    10**(2*sigma + np.log10(inventory)),
                    10**(-2*sigma + np.log10(inventory)),
                    facecolor=line.get_color(), alpha=0.3)

        plt.legend()

    def show(self):
        """Similar to matplotlib.pyplot.show()
        """
        plt.show()


def create_correspondance_dict(filename, filetype):
    """Creates a correspondance dictionary link for the case

    Args:
        filename (str): The CSV file name.
        filetype (str): The CSV file type
            ("WEST" or "ITER").

    Returns:
        dict: correspondance dictionary with a "var" key for each quantity
    """
    my_exposition = Exposition(filename, filetype)
    correspondance_dict["arc_length"]["var"] = my_exposition.arc_length
    correspondance_dict["ion_energy"]["var"] = my_exposition.E_ion
    correspondance_dict["atom_energy"]["var"] = my_exposition.E_atom
    correspondance_dict["ion_flux"]["var"] = my_exposition.ion_flux
    correspondance_dict["atom_flux"]["var"] = my_exposition.atom_flux
    correspondance_dict["heat_flux"]["var"] = my_exposition.net_heat_flux
    correspondance_dict["ion_angle"]["var"] = my_exposition.angles_ions
    correspondance_dict["atom_angle"]["var"] = my_exposition.angles_atoms
    correspondance_dict["T_surf"]["var"] = my_exposition.temperature
    correspondance_dict["c_surf"]["var"] = my_exposition.concentration
    correspondance_dict["inventory"]["var"] = my_exposition.inventory
    correspondance_dict["stdev_inv"]["var"] = my_exposition.stdev_inv

    return correspondance_dict


class plot_T_c_inv_along_divertor(plot_along_divertor):
    """Plots the temperature, concentration and inventory distribution along
    the divertor
    """
    def __init__(self, **kwargs):
        super().__init__(
            quantities=["T_surf", "c_surf", "inventory"],
            **kwargs)


class plot_particle_exposure_along_divertor(plot_along_divertor):
    """Plots the exposure condition (particle fluxes, energies and angles)
    along the divertor
    """
    def __init__(self, **kwargs):
        quantities = [
            "atom_flux", "ion_flux",
            "ion_energy", "atom_energy",
            "ion_angle", "atom_angle",
            ]
        super().__init__(
            quantities=quantities,
            **kwargs)


def plot_inv_with_uncertainty(x, y, stdev, zscore=2, alpha_fill=0.3, **kwargs):
    """Plots the inventory along the divertor with the associated uncertainity
    filled

    Args:
        x (numpy.array): Arc length (m) along the divertor
        y (numpy.array): Inventory per unit thickness (H/m) 
        stdev (numpy.array): standard deviation
        zscore (float): userdefined zscore corresponding to a confidence interval. Defaults to 2.
        alpha_fill (float, optional): Opacity of the filled region between 0 and 1. Defaults to 0.3.
    """
    # check that zscore is a float
    if type(zscore) not in [float, int]:
        raise TypeError("zscore should be a float")
    line, = plt.plot(x, y, **kwargs)
    plt.fill_between(
        x,
        10**(zscore*stdev + np.log10(y)),
        10**(-zscore*stdev + np.log10(y)),
        facecolor=line.get_color(), alpha=alpha_fill)
