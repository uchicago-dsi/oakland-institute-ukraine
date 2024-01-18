# Name: Josemaria Macedo Carrillo
# Title: Read data
# Created: 07/18/23
# Last modified: 01/17/24
# DSI

import os
import pandas as pd
from .clean_data import rename_columns, create_columns, translate_column, clean_column
import re

CURRENT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# def get_data(path, source):
#     """
#     Import data from .csv file name

#     Inputs:
#         path (str): path for data file
#         source (str): data source, either "ig" (Import Genius), "bsgi" (Black
#             Sea Grain Initiative) or panjiva.

#     Return (DataFrame): dataframe.
#     """

#     if source == "ig":
#         df = pd.read_csv(path, parse_dates=["EXPORT DATE"], encoding = "utf-8")
#         # Add 0 to HS Codes that have 9 digits because apparently Import Genius
#         # cuts the 0 at the beggining 
#         df["HS CODE"] = df["HS CODE"].astype(str)
#         df["HS CODE"] = df["HS CODE"].apply(lambda x: "0" + x if len(x) == 9 else x)
    
#     elif source == "bsgi":
#         df = pd.read_csv(path, thousands=",", parse_dates=["Departure date"])

#     elif source == "panjiva":
#         df = pd.read_excel(path, parse_dates=["Date"])

#     return df

def compile_data(directory_name):
    """
    Compile data files into one dataframe

    Inputs:
        directory_name (str): name of directory where data files are located.
    
    Return (DataFrame): dataframe with compiled data
    """
    path = os.path.join(CURRENT_DIR, "data", directory_name)
    
    if directory_name == "bsgi":
        return get_data(os.path.join(path, "bsgi_outbound.csv"), directory_name)
    elif directory_name == "ig":
        path = os.path.join(path, "company_files")
    
    file_formats = ["xlsx", "csv"]
    compiled_df = pd.DataFrame()

    for file in os.listdir(path):
        if re.split("_|\\.", file)[-1] in file_formats:
            file_path = os.path.join(path, file)
            df = get_data(file_path, directory_name)
            df["company_searched"] = re.split("_|\\.", file)[1]
            if directory_name == "ig":
                df["search_batch"] = re.split("_|\\.", file)[2]
            compiled_df = pd.concat([compiled_df, df])

    return compiled_df