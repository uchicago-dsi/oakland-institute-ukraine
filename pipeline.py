# Name: Josemaria Macedo Carrillo
# Title: Data pipeline
# Created: 01/11/24
# Last modified: 01/17/24
# DSI

import pandas as pd
from config import IG_FILES_PATH, COUNTRY_FILES
from utils.clean_data import generate_path, clean_data, correct_name,\
    create_subsidiary_dict, ASIA_NAME_DICT,\
    SPAIN_NAME_DICT, BELGIUM_NAME_DICT
from utils.transform_data import standard_company_name
import os
import sys
import argparse

def clean_ig_by_country(countries, save=True):
    """
    Get Import Genius (IG) data for specific countries.

    Inputs:
        countries (str): countries which we want the path for. It can be either
            'asia', 'spain' or 'belgium'.

    Returns (DataFrame): table with filtered Import Genius data.
    """
    path = generate_path(countries)
    ig = clean_data("ig", path)

    if countries == "asia":
        country_name_dict = ASIA_NAME_DICT
    elif countries == "spain":
        country_name_dict = SPAIN_NAME_DICT
    elif countries == "belgium":
        country_name_dict = BELGIUM_NAME_DICT

    # We standardize the "country" values in the IG dataset
    ig["country"] = correct_name(ig["country"], country_name_dict)

    # We only keep crops that are included both in IG and BSGI
    ig = ig[ig["bsgi_commodity"]!= "Not in BSGI"]

    subsidiaries_dict = create_subsidiary_dict(25, 20, ig)
    ig_c = ig.copy()
    ig_c["company_std"] = standard_company_name(ig["shipper_low"], subsidiaries_dict)

    # Save clean IG dataset in "/data" directory
    if save:
        file_name = f"ig_clean_{countries}.csv"
        export_path = os.path.join(os.path.dirname(path), file_name)
        ig_c.to_csv(export_path, index=False)

    return ig_c


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="My parser")
    parser.add_argument("country", type=str,
                        help="Options are 'spain', 'belgium' and 'asia'")
    parser.add_argument("--clean", type=bool,
                        help="Cleans data and saves file by default",
                        default=True)
    # group = parser.add_mutually_exclusive_group(required=False)
    # group.add_argument("--clean", action="store_true")
    # group.add_argument("--visualize", action="store_true")
    # group.add_argument("--run_all", action="store_true")
    # parser.add_argument("save", type=bool, help="Save clean files. Default is true",
    #                     default=True)

    # parser.set_defaults(clean=False, visualize=False, run_all=True)

    args = parser.parse_args()

    if args.clean:
        clean_ig_by_country(args.country)