import divHretention
import numpy as np


def test_exposition_ITER():
    """Test Exposition with ITER file
    """
    # build
    filename = "data/example_ITER.csv"
    arc_length = np.linspace(0, 1)
    Te = np.linspace(1, 2)
    Ti = np.linspace(1, 2)
    D_temp_atm = np.linspace(1, 2)
    D_flux_atm = np.linspace(1, 2)
    D_flux_ion = np.linspace(1, 2)
    Wtot = np.linspace(1, 2)
    header = "x,Te,Ti,D_temp_atm,D_flux_ion,D_flux_atm,Wtot"
    data = np.asarray([arc_length, Te, Ti, D_temp_atm, D_flux_ion, D_flux_atm, Wtot]).T
    np.savetxt(filename, data, delimiter=",", header=header)

    # run
    my_exposure = divHretention.Exposition(filename, "ITER")
