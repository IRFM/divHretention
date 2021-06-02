# import matplotlib.pyplot as plt

from main import plot_Tc_map_with_subplots

filename = "data/exposure_conditions_divertor/WEST/West-LSN-P2.5e+21-IP0.449MW.csv"

my_plot = plot_Tc_map_with_subplots(filenames=[filename], T_bounds=[320, 400], figsize=(5, 5))
my_plot.axs_bottom[1].get_yaxis().set_ticks([])
my_plot.axs_top[1].yaxis.set_label_position("right")
my_plot.axs_top[1].yaxis.tick_right()
my_plot.show()
