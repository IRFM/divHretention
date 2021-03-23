from main import plot_Tc_map_with_subplots, \
    plot_T_c_inv_along_divertor, plot_particle_exposure_along_divertor, \
    plot_along_divertor, extract_data
import matplotlib.pyplot as plt

filenames = [
    "data/exposure_conditions_divertor/WEST/Hao/P1.0e21_wall_data.mat",
    "data/exposure_conditions_divertor/WEST/Julien/WPN54696-1.5MW-FESTIM_inputs.csv"
]

quantities = [
    "heat_flux",
    "ion_flux", "atom_flux",
    "ion_energy", "atom_energy",
    "ion_angle", "atom_angle"
]
my_plot = plot_along_divertor(filenames=[filenames[1]], quantities=quantities)
plt.show()