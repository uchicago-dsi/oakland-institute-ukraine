# Name: Josemaria Macedo Carrillo
# Title: Data pipeline
# Created: 01/11/24
# Last modified: 01/17/24
# DSI

import pandas as pd
from config import IG_FILES_PATH, COUNTRY_FILES
from utils.clean_data import generate_path, clean_data, correct_name,\
    create_subsidiary_dict, standard_company_name, ASIA_NAME_DICT,\
    SPAIN_NAME_DICT, BELGIUM_NAME_DICT
import os
import sys

def get_data(path, source):
    """
    Import data from .csv file name

    Inputs:
        path (str): path for data file
        source (str): data source, either "ig" (Import Genius), "bsgi" (Black
            Sea Grain Initiative) or panjiva.

    Return (DataFrame): dataframe.
    """

    if source == "ig":
        df = pd.read_csv(path, parse_dates=["EXPORT DATE"], encoding = "utf-8")
        # Add 0 to HS Codes that have 9 digits because apparently Import Genius
        # cuts the 0 at the beggining 
        df["HS CODE"] = df["HS CODE"].astype(str)
        df["HS CODE"] = df["HS CODE"].apply(lambda x: "0" + x if len(x) == 9 else x)
    
    elif source == "bsgi":
        df = pd.read_csv(path, thousands=",", parse_dates=["Departure date"])

    elif source == "panjiva":
        df = pd.read_excel(path, parse_dates=["Date"])

    return df

def clean_ig_by_country(countries):
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
    file_name = f"ig_clean_{countries}.csv"
    export_path = os.path.join(os.path.dirname(path), file_name)
    ig_c.to_csv(export_path, index=False)

    return ig_c


if __name__ == "__main__":

    if len(sys.argv) == 1:
        # Plot data in jupyter notebook with specified country (does the same
        # as sending 'plot' as second argument)

    elif len(sys.argv) == 2:
        if sys.argv[1] == "import_data":
            # Function to import data
        elif sys.argv[1] == "clean_data":
            # Function to clean data
        elif sys.argv[1] == "transform_data":
            # Function to transform data
        elif sys.argv[1] == "plot":
            # Plot data in jupyter notebook
        elif sys.argv[1] == "run_all":
            # Function to run the whole data pipeline for that country 
        else:
            print("Incorrect arguments. Send 'import_data', 'clean_data',\
                  'transform_data', 'plot' or 'run_all'.")