import sys
sys.path.append('.')

import pandas as pd
from utils.clean_data import keep_chr, rename_columns, translate_column
from utils.record_linkage import find_matches
from utils.plot import cargo_grouping, plot_line, plot_crops

pd.set_option('display.float_format', lambda x: '%.4f' % x)

# Import data
ig = pd.read_csv("../data/import_genius/kernel_10000.csv", parse_dates=["EXPORT DATE"])

## Rename columns so they have standardized column name format (lowercase, no
# spaces and no special characters)
ig_c = ig.copy()
ig_c = rename_columns(ig_c)


# Create columns with specific formats
kernel_c["year"] = kernel_c["export_date"].dt.year
kernel_c["month"] = kernel_c["export_date"].dt.month
kernel_c["weight_ton"] = kernel_c["weight_kg"] / 1000
kernel_g["date"] = kernel_g["month"].astype(str) + "/" + kernel_g["year"].astype(str)


outbound["year"] = outbound["departure_date"].dt.year
outbound["month"] = outbound["departure_date"].dt.month
outbound = outbound.rename(columns={"metric_tons": "weight_ton"})
outbound_g["date"] = outbound_g["month"].astype(str) + "/" + outbound_g["year"].astype(str)


kernel_g = cargo_grouping(kernel_c, ["year", "month"], ["weight_ton"], ["year", "month"], True)
plot_line(kernel_g["date"], [kernel_g["weight_ton"]], ["Kernel"], "Kernel's volume of exports", "Export date (m-yy)", "Products exported (tons)")