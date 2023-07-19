# Name: Josemaria Macedo Carrillo
# Title: App file
# Created: 07/18/23
# Last modified: -
# DSI

import os
import pandas as pd
from utils.clean_data import rename_columns, create_columns, translate_column
from utils.record_linkage import find_matches
from utils.plot import cargo_grouping, plot_line, plot_crops

pd.set_option('display.float_format', lambda x: '%.4f' % x)

# Import data
# ADD THIS LATER AS FUNCTION IN READ_DATA MODULE
current_dir = os.path.dirname(os.path.abspath(__file__))
ig_path = os.path.join(current_dir, "data/import_genius/kernel_10000.csv")
bsgi_path = os.path.join(current_dir, "data/bsgi_outbound_shipments.csv")

ig = pd.read_csv(ig_path, parse_dates=["EXPORT DATE"])
bsgi = pd.read_csv(bsgi_path, thousands=",", parse_dates=["Departure date"])

## Rename columns so they have standardized column name format (lowercase, no
# spaces and no special characters)
ig_c = ig.copy()
bsgi_c = bsgi.copy()
ig_c = rename_columns(ig_c)
bsgi_c = rename_columns(bsgi_c)
bsgi_c = bsgi_c.rename(columns={"metric_tons": "weight_ton"})

# Create columns with specific formats
create_columns(ig_c, "ig")
create_columns(bsgi_c, "bsgi")

# Create graph image outputs and save them in "output" directory
# Graph 1. Total volume of exports from Import Genius and BSGI
ig_g = cargo_grouping(ig_c, ["year", "month"], ["weight_ton"], ["year", "month"], True)
bsgi_g = cargo_grouping(bsgi_c, ["year", "month"], ["weight_ton"], ["year", "month"], True)
ig_g["date"] = ig_g["month"].astype(str) + "/" + ig_g["year"].astype(str)
bsgi_g["date"] = bsgi_g["month"].astype(str) + "/" + bsgi_g["year"].astype(str)

graph_1 = ig_g.merge(bsgi_g, on="date", suffixes=("_ig", "_bsgi"))
plot_line(graph_1["date"], [graph_1["weight_ton_ig"], graph_1["weight_ton_bsgi"]], ["Kernel", "Black Sea Grain Initiative"], "BSGI and Kernel volume of exports", "Export date (m-yy)", "Products exported (tons)")

# Graph 2. Total volume of exports from Import Genius