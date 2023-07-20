# Name: Josemaria Macedo Carrillo
# Title: App file
# Created: 07/17/23
# Last modified: 07/20/23
# DSI

import os
import pandas as pd
from utils.get_data import get_data
from utils.clean_data import PRODUCTS_VAL
from utils.plot import cargo_grouping, plot_line, plot_crops

pd.set_option('display.float_format', lambda x: '%.4f' % x)

# Import clean data
ig = get_data("ig_kernel_10000.csv", "ig")
bsgi = get_data("bsgi_outbound_shipments.csv", "bsgi")

# Create graph image outputs and save them in "output" directory
# Graph 1. Total volume of exports from Import Genius and BSGI
ig_g = cargo_grouping(ig, ["year", "month"], ["weight_ton"], ["year", "month"], True)
bsgi_g = cargo_grouping(bsgi, ["year", "month"], ["weight_ton"], ["year", "month"], True)
ig_g["date"] = ig_g["month"].astype(str) + "/" + ig_g["year"].astype(str)
bsgi_g["date"] = bsgi_g["month"].astype(str) + "/" + bsgi_g["year"].astype(str)

graph_1 = ig_g.merge(bsgi_g, on="date", suffixes=("_ig", "_bsgi"))
plot_line(graph_1["date"], [graph_1["weight_ton_ig"], graph_1["weight_ton_bsgi"]], ["Kernel", "Black Sea Grain Initiative"], "BSGI and Kernel volume of exports", "Export date (m-yy)", "Products exported (tons)", True)

# Graph 2. Total volume of exports from Import Genius and BSGI per crop
product_std = set(PRODUCTS_VAL)

for crop in product_std:
    plot_crops(crop, ig, bsgi, True)
