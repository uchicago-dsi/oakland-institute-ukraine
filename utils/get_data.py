# Name: Josemaria Macedo Carrillo
# Title: Read data
# Created: 07/18/23
# Last modified: 07/26/23
# DSI

import os
import pandas as pd
from .clean_data import rename_columns, create_columns, translate_column, clean_column
import re

CURRENT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def import_data(path, source):
    """
    Import data from .csv file name

    Inputs:
        path (str): path for data file
        source (str): data source, either "ig" (Import Genius) or "bsgi" (Black
            Sea Grain Initiative).

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

def compile_data(directory_name):
    """
    Compile data files into one dataframe

    Inputs:
        directory_name (str): name of directory where data files are located.
    
    Return (DataFrame): dataframe with compiled data
    """
    path = os.path.join(CURRENT_DIR, "data", directory_name)
    
    if directory_name == "bsgi":
        return import_data(os.path.join(path, "bsgi_outbound.csv"), directory_name)
    
    file_formats = ["xlsx", "csv"]
    compiled_df = pd.DataFrame()

    for file in os.listdir(path):
        if re.split("_|\\.", file)[-1] in file_formats:
            file_path = os.path.join(path, file)
            df = import_data(file_path, directory_name)
            df["company_searched"] = re.split("_|\\.", file)[1]
            if directory_name == "ig":
                df["search_batch"] = re.split("_|\\.", file)[2]
            compiled_df = pd.concat([compiled_df, df])

    return compiled_df

def get_data(source, path=None):
    """
    Get clean data from data source directory
    Inputs:
        source (str): data source, either "ig" (Import Genius), "bsgi" (Black
            Sea Grain Initiative) or "panjiva".

    Return (DataFrame): dataframe with cleaned data (with renamed columns and
        new columns neccesary for analysis).
    """
    data_sources = ["ig", "bsgi", "panjiva"]
    assert source in data_sources, "Wrong data source Error: source must be\
                                    'ig', 'bsgi' or 'panjiva'."
    
    if path is None:
        df = compile_data(source)
    else:
        df = import_data(path, source)
        if source == "ig":
            df["company_searched"] = df["SHIPPER"]
    df = rename_columns(df, source)
    create_columns(df, source)
    
    columns = ["country", "product"]
    for col in columns:
        clean_column(df, col)

    if source == "bsgi":
        translate_column(df, "product_std", "google", "en", "uk")
        translate_column(df, "country", "google", "en", "uk")
        df = df.rename(columns={"country": "country_en",
                                "country_gt": "country"})
        clean_column(df, "country")

    elif source == "panjiva":
        clean_column(df, "shipment_origin")
        df = df.loc[df.loc[:, "shipment_origin"] == "ukraine"]

    return df