try:
    import importlib.resources as pkg_resources
except ImportError:
    # Try backported to PY<37 `importlib_resources`.
    import importlib_resources as pkg_resources

from . import data as mb_data  # relative-import the *package* containing the templates
filename = "data_TRIM_energy_angle.csv"
with pkg_resources.path(mb_data, filename) as p:
    filename = p
filename = str(filename)
folder_mb_data = filename.replace(r"\data_TRIM_energy_angle.csv", "")

from .compute_implantation_coefficients_angle import \
    implantation_range, reflection_coeff
from .extract_data import Exposition
from .inventory_T_c import estimate_inventory_with_gp_regression
from .compute_inventory import process_file, compute_c_max, \
    compute_inventory, DEFAULT_TIME, database_inv_sig

from .plotting.plot_2d_contour import plot_Tc_map_with_subplots, \
    create_2d_inv_array
from .plotting.plot_along_divertor import \
    plot_T_c_inv_along_divertor, plot_particle_exposure_along_divertor, \
    plot_along_divertor
