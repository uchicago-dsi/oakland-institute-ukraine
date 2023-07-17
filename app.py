import sys
sys.path.append('.')

import pandas as pd
from utils.clean_data import keep_chr, rename_columns, translate_column
from utils.record_linkage import find_matches
from utils.plot import cargo_grouping, plot_line, plot_crops

pd.set_option('display.float_format', lambda x: '%.4f' % x)

kernel = pd.read_csv("../data/import genius/kernel_10000.csv", parse_dates=["EXPORT DATE"])

## Rename columns so they have standardized column name format (lowercase, no
# spaces and no special characters)
kernel = rename_columns(kernel)
kernel_c = kernel.copy()
translate_column(kernel_c, "product", "google")
translate_column(kernel_c, "product", "deepl")

kernel_c["year"] = kernel_c["export_date"].dt.year
kernel_c["month"] = kernel_c["export_date"].dt.month
kernel_c["weight_ton"] = kernel_c["weight_kg"] / 1000

kernel_g = cargo_grouping(kernel_c, ["year", "month"], ["weight_ton"], ["year", "month"], True)
kernel_g["date"] = kernel_g["month"].astype(str) + "/" + kernel_g["year"].astype(str)