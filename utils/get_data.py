# Name: Josemaria Macedo Carrillo
# Title: Read data
# Created: 07/18/23
# Last modified: 07/19/23
# DSI

import os
import pandas as pd
from .clean_data import rename_columns, create_columns, translate_column, clean_column

def import_data(file_name, source):
    """
    Import data from .csv file name

    Inputs:
        file_name (str): name of the .csv file
        source (str): data source, either "ig" (Import Genius) or "bsgi" (Black
            Sea Grain Initiative).

    Return (DataFrame): dataframe.
    """

    current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    path = os.path.join(current_dir, "data/", file_name)

    if source == "ig":
        df = pd.read_csv(path, parse_dates=["EXPORT DATE"])
    
    else:
        df = pd.read_csv(path, thousands=",", parse_dates=["Departure date"])
    
    return df

def get_data(file_name, source):
    """
    Get clean data from .csv file name

    Inputs:
        file_name (str): name of the .csv file
        source (str): data source, either "ig" (Import Genius) or "bsgi" (Black
            Sea Grain Initiative).

    Return (DataFrame): dataframe with cleaned data (with renamed columns and
        new columns neccesary for analysis).
    """
    assert source == "ig" or source == "bsgi", "Wrong data source Error: source\
                                                must be either 'ig' or 'bsgi'."
    
    df = import_data(file_name, source)
    df = rename_columns(df, source)
    create_columns(df, source)
    
    columns = ["country", "product"]
    for col in columns:
        clean_column(df, col)

    if source == "bsgi":
        translate_column(df, "product_std", "google", "en", "uk")

    return df

    
