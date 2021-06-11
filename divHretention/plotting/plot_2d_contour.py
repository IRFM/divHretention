import matplotlib.pyplot as plt
from matplotlib import ticker
import numpy as np

from divHretention import DEFAULT_TIME, database_inv_sig, fetch_inventory_and_error, Exposition


class plot_Tc_map_with_subplots():
    """Plots the (T, concentration) map with distribution plots on the side.
    This class works with csv files (see :func:`Exposition()
    <divHretention.extract_data.Exposition>`)

    Args:
        filenames (list, optional): The CSV file names. Defaults to [].
        filetypes (list, optional): The CSV file types ("WEST" or "ITER").
            Defaults to [].
        T_bounds (list, optional): The limits for T (K).
            Defaults to [320, 1200].
        c_bounds (list, optional): The limits for concentration (H m-3).
            Defaults to [1e20, 1e23].
        figsize (tuple, optional): The size of the figure. Defaults to (8, 8).
    """
    def __init__(
            self, filenames=[], filetypes=[], time=DEFAULT_TIME, T_bounds=[320, 1200],
            c_bounds=[1e20, 1e23], figsize=(8, 8), **kwargs):

        self.fig, (self.axs_top, self.axs_bottom) = \
            plt.subplots(
                figsize=figsize, nrows=2,
                ncols=2, sharex="col", **kwargs)
        self.count = 0
        self.filenames = filenames[:]
        if type(filetypes) is str:
            self.filetypes = [filetypes for _ in filenames]
        else:
            self.filetypes = filetypes[:]

        self.time = time
        self.T_bounds = T_bounds
        self.c_bounds = c_bounds

        self.plot_2d_map()
        for filename, filetype in zip(self.filenames, self.filetypes):
            self.add_case(filename, filetype)

    @property
    def T_bounds(self):
        return self._T_bounds

    @T_bounds.setter
    def T_bounds(self, value):
        self._T_bounds = value
        if hasattr(self, "c_bounds"):
            self.plot_2d_map()

    @property
    def c_bounds(self):
        return self._c_bounds

    @c_bounds.setter
    def c_bounds(self, value):
        self._c_bounds = value
        if hasattr(self, "T_bounds"):
            self.plot_2d_map()
            self.axs_bottom[1].set_ylim(self.c_bounds[0], self.c_bounds[1])

    def plot_2d_map(self):
        self.axs_bottom[0].cla()
        plt.sca(self.axs_bottom[0])
        x = np.linspace(*self.T_bounds, num=50)
        y = np.logspace(np.log10(self.c_bounds[0]), np.log10(self.c_bounds[1]), num=10)
        XX, YY = np.meshgrid(x, y)
        values, levels = create_2d_inv_array(XX, YY, time=self.time)
        plt.xlim(*self.T_bounds)
        plt.ylim(*self.c_bounds)

        # plot the inventory contour
        locator = ticker.LogLocator(base=10)
        self.CS = plt.contourf(XX, YY, values, locator=locator, levels=levels)
        for c in self.CS.collections:
            c.set_edgecolor("face")
        # plt.colorbar(CS, label=r"Inventory per monoblock (H)", ticks=locator)
        plt.yscale("log")
        plt.tick_params(axis='both', which='major')
        plt.xlabel(r"$T_\mathrm{surface}$ (K)")
        plt.ylabel(r"$c_\mathrm{surface}$ (m$^{-3}$)")

    def add_case(self, filename, filetype):
        """Adds a new exposure case to the plot.

        Args:
            filename (str): The CSV file name.
            filetype (str): The CSV file type
                ("WEST" or "ITER").
        """
        self.count += 1
        self.filenames.append(filename)
        xlabel = "Distance along divertor (m)"
        res = Exposition(filename, filetype)
        plt.sca(self.axs_bottom[0])
        plt.plot(res.temperature, res.concentration, alpha=0.7)
        plt.sca(self.axs_bottom[1])
        plt.xlabel(xlabel)
        plt.yscale("log")
        plt.plot(res.arc_length, res.concentration, label="Case {}".format(self.count))
        plt.sca(self.axs_top[0])
        plt.ylabel(xlabel)
        plt.plot(res.temperature, res.arc_length, label="Case {}".format(self.count))
        plt.sca(self.axs_top[1])
        line, = plt.plot(res.arc_length, res.inventory, label="Case {}".format(self.count))

        plt.fill_between(
            res.arc_length,
            10**(2*res.stdev_inv + np.log10(res.inventory)),
            10**(-2*res.stdev_inv + np.log10(res.inventory)),
            facecolor=line.get_color(), alpha=0.3)
        plt.ylabel("Inventory per unit thickness (H/m)")
        plt.yscale("log")
        plt.tight_layout()

    def show(self):
        """Similar to matplotlib.pyplot.show()
        """
        plt.show()


def create_2d_inv_array(XX, YY, time=DEFAULT_TIME):
    values = np.zeros(XX.shape)
    min_value, max_value = float("inf"), float("-inf")
    for i in range(len(XX)):
        for j in range(len(XX[i])):
            inventory = fetch_inventory_and_error(time)[0]
            val = inventory(XX[i][j], YY[i][j])
            values[i][j] = val
            min_value = min(min_value, float(val))
            max_value = max(max_value, float(val))
    levels = np.logspace(
        np.log10(min_value),
        np.log10(max_value),
        1000)
    return values, levels
